import { useEffect, useMemo, useState } from "react";
import { VoicePoweredOrb } from "@/components/ui/voice-powered-orb";

type JarvisState = "idle" | "speaking" | "listening" | "processing";

type JarvisMessage = {
  state: JarvisState;
  message: string;
  level: number;
};

const STATE_CONFIG: Record<
  JarvisState,
  { activity: number; hue: number; glow: string }
> = {
  idle: {
    activity: 0.06,
    hue: 0,
    glow: "rgba(88,72,180,0.10)",
  },
  speaking: {
    activity: 0.9,
    hue: 16,
    glow: "rgba(121,88,255,0.22)",
  },
  listening: {
    activity: 0.65,
    hue: -28,
    glow: "rgba(58,158,255,0.18)",
  },
  processing: {
    activity: 1,
    hue: 35,
    glow: "rgba(157,89,255,0.24)",
  },
};

export default function App() {
  const [jarvis, setJarvis] = useState<JarvisMessage>({
    state: "idle",
    message: "Connexion à Jarvis…",
    level: 0,
  });
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    let socket: WebSocket | null = null;
    let retryTimer: number | undefined;
    let stopped = false;

    const connect = () => {
      if (stopped) return;

      socket = new WebSocket("ws://127.0.0.1:8765");

      socket.addEventListener("open", () => {
        setConnected(true);
      });

      socket.addEventListener("message", (event) => {
        try {
          const next = JSON.parse(event.data) as Partial<JarvisMessage>;
          if (
            next.state &&
            ["idle", "speaking", "listening", "processing"].includes(next.state)
          ) {
            setJarvis({
              state: next.state as JarvisState,
              message: next.message || "",
              level:
                typeof next.level === "number"
                  ? Math.max(0, Math.min(next.level, 1))
                  : 0,
            });
          }
        } catch {
          // Ignore malformed local state messages.
        }
      });

      socket.addEventListener("close", () => {
        setConnected(false);
        if (!stopped) {
          retryTimer = window.setTimeout(connect, 1200);
        }
      });

      socket.addEventListener("error", () => {
        socket?.close();
      });
    };

    connect();

    return () => {
      stopped = true;
      window.clearTimeout(retryTimer);
      socket?.close();
    };
  }, []);

  const config = useMemo(() => STATE_CONFIG[jarvis.state], [jarvis.state]);
  const orbActivity =
    jarvis.state === "speaking"
      ? Math.max(0.08, jarvis.level)
      : config.activity;

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-black">
      <div
        className="pointer-events-none absolute inset-0 transition-all duration-700"
        style={{
          background: `radial-gradient(circle at center, ${config.glow}, transparent 42%)`,
        }}
      />

      <section className="relative z-10 flex flex-col items-center">
        <div className="relative h-[min(62vw,520px)] w-[min(62vw,520px)] min-h-[300px] min-w-[300px]">
          <div className="absolute inset-[14%] rounded-full bg-violet-500/10 blur-[80px]" />
          <VoicePoweredOrb
            className="relative z-10 h-full w-full"
            hue={config.hue}
            activity={orbActivity}
            state={jarvis.state}
          />
        </div>

        <div className="-mt-8 flex flex-col items-center gap-2 text-center">
          <p className="text-[11px] font-medium uppercase tracking-[0.42em] text-white/30">
            Jarvis
          </p>
          <p className="min-h-5 text-sm font-normal tracking-[0.01em] text-white/65">
            {connected ? jarvis.message : "Jarvis hors ligne"}
          </p>
        </div>
      </section>

      <div className="absolute bottom-7 left-1/2 flex -translate-x-1/2 items-center gap-2 text-[10px] tracking-[0.18em] text-white/20">
        <span
          className={`h-1.5 w-1.5 rounded-full ${
            connected ? "bg-emerald-400/60" : "bg-white/20"
          }`}
        />
        <span>{connected ? "DOUBLE CLAP TO WAKE" : "PYTHON OFFLINE"}</span>
      </div>
    </main>
  );
}
