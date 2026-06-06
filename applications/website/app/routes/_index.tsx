import Hero from "../components/landing/Hero"
import HowItWorks from "../components/landing/HowItWorks"
import Features from "../components/landing/Features"
import OpenSource from "../components/landing/OpenSource"
import Footer from "../components/landing/Footer"

export default function Index() {
  return (
    <div className="bg-coffee-bg min-h-screen text-coffee-text selection:bg-coffee-accent/20 selection:text-coffee-text font-sans antialiased overflow-x-hidden">
      <Hero />
      <HowItWorks />
      <Features />
      <OpenSource />
      <Footer />
    </div>
  )
}
