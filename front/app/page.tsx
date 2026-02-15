"use client"

import { Canvas, useFrame, useLoader } from "@react-three/fiber"
import { OrbitControls, Stars } from "@react-three/drei"
import { TextureLoader } from "three"
import { useRef } from "react"
import * as THREE from "three"
import { motion } from "framer-motion"
import { useRouter } from "next/navigation"

function Earth() {
  const meshRef = useRef<THREE.Mesh>(null!)
  const texture = useLoader(TextureLoader, "/earth_atmos_2048.jpg")

  useFrame(({ clock }) => {
    meshRef.current.rotation.y += 0.0015
    meshRef.current.position.y = Math.sin(clock.elapsedTime) * 0.08
  })

  return (
    <>
      <mesh ref={meshRef}>
        <sphereGeometry args={[1.7, 128, 128]} />
        <meshStandardMaterial map={texture} />
      </mesh>

      {/* Atmosphere Glow */}
      <mesh>
        <sphereGeometry args={[1.9, 128, 128]} />
        <meshStandardMaterial
          color="#8ab4f8"
          transparent
          opacity={0.06}
          side={THREE.BackSide}
        />
      </mesh>
    </>
  )
}

function FloatingLight() {
  const lightRef = useRef<THREE.PointLight>(null!)

  useFrame(({ clock }) => {
    lightRef.current.intensity = 1.5 + Math.sin(clock.elapsedTime * 2) * 0.3
  })

  return (
    <pointLight
      ref={lightRef}
      position={[0, 0, 3]}
      color="#8ab4f8"
      intensity={1.5}
    />
  )
}

/* ✨ Fake shooting star */
function ShootingStar() {
  const starRef = useRef<THREE.Mesh>(null!)

  useFrame(({ clock }) => {
    const t = clock.elapsedTime

    starRef.current.position.x = (t * 2) % 20 - 10
    starRef.current.position.y = 5 - ((t * 2) % 10)
  })

  return (
    <mesh ref={starRef}>
      <sphereGeometry args={[0.03]} />
      <meshBasicMaterial color="white" />
    </mesh>
  )
}

export default function Home() {
  const router = useRouter()

  return (
    <main
      style={{
        height: "100vh",
        background: "black",
        overflow: "hidden",
        position: "relative",
      }}
    >
      {/* Canvas */}
      <Canvas camera={{ position: [0, 0, 6] }}>

        <ambientLight intensity={0.25} />

        <directionalLight
          position={[3, 2, 5]}
          intensity={1.2}
        />

        <directionalLight
          position={[-3, -2, -5]}
          intensity={0.3}
          color="#8ab4f8"
        />

        <FloatingLight />
        <Earth />

        {/* 🌟 Background stars */}
        <Stars
          radius={100}
          depth={50}
          count={4000}
          factor={4}
          saturation={0}
          fade
        />

        {/* 💫 Shooting star */}
        <ShootingStar />

        <OrbitControls enableZoom={false} enablePan={false} />
      </Canvas>

      {/* Center Panel */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          pointerEvents: "none",
        }}
      >
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.2 }}
          style={{
            background: "rgba(15, 23, 42, 0.55)",
            border: "1px solid rgba(138,180,248,0.18)",
            padding: "60px 100px",
            borderRadius: "26px",
            backdropFilter: "blur(22px)",
            boxShadow: "0 0 140px rgba(138,180,248,0.12)",
            textAlign: "center",
          }}
        >
          <motion.h1
            animate={{ opacity: [0.7, 1, 0.7] }}
            transition={{ duration: 4, repeat: Infinity }}
            style={{
              fontSize: "3.3rem",
              color: "#e5e7eb",
              margin: 0,
              fontWeight: 500,
            }}
          >
            APK Omen
          </motion.h1>

          <motion.p
            animate={{ opacity: [0.4, 0.7, 0.4] }}
            transition={{ duration: 5, repeat: Infinity }}
            style={{
              color: "rgba(255,255,255,0.55)",
              marginTop: "18px",
            }}
          >
            Sovereign Mobile Threat Intelligence
          </motion.p>
        </motion.div>
      </div>

      {/* 🚀 Floating Tabs */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
        }}
      >
      

        <div className="tab dev" onClick={() => router.push("/dev")}>
          DEV SCAN
        </div>

        <div className="tab defense" onClick={() => router.push("/defense")}>
          ADMIN
        </div>
      </div>
    </main>
  )
}
