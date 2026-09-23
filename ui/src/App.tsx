import { useState } from "react";
import { VoicePoweredOrb } from "@/components/ui/voice-powered-orb";

export default function App() {
  const [voiceDetected, setVoiceDetected] = useState(false);

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-black">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(88,72,180,0.10),transparent_42%)]" />

      <section className="relative z-10 flex flex-col items-center">
        <div className="relative h-[min(62vw,520px)] w-[min(62vw,520px)] min-h-[300px] min-w-[300px]">
          <div className="absolute inset-[14%] rounded-full bg-violet-500/10 blur-[80px]" />
          <VoicePoweredOrb
            className="relative z-10 h-full w-full"
            hue={0}
            enableVoiceControl
            voiceSensitivity={1.25}
            maxRotationSpeed={0.9}
            maxHoverIntensity={0.65}
            onVoiceDetected={setVoiceDetected}
          />
        </div>

        <div className="-mt-8 flex flex-col items-center gap-2 text-center">
          <p className="text-[11px] font-medium uppercase tracking-[0.42em] text-white/30">
            Jarvis
          </p>
          <p className="text-sm font-normal tracking-[0.01em] text-white/65">
            {voiceDetected ? "Je vous écoute…" : "En attente"}
          </p>
        </div>
      </section>

      <p className="absolute bottom-7 left-1/2 -translate-x-1/2 text-[10px] tracking-[0.18em] text-white/20">
        DOUBLE CLAP TO WAKE
      </p>
    </main>
  );
}
