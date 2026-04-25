import React from "react";
import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <div className="text-on-surface bg-surface-container-lowest min-h-screen font-sans selection:bg-primary selection:text-on-primary">
      {/* Top Navigation */}
      <header className="sticky top-0 z-50 w-full glass-panel border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center">
            <span className="text-2xl font-black tracking-tighter bg-linear-to-r from-primary to-secondary bg-clip-text text-transparent">
              WebSpector
            </span>
          </div>
          <nav className="hidden md:flex items-center gap-10">
            <a
              className="text-on-surface-variant hover:text-white text-sm font-medium transition-colors"
              href="#features"
            >
              Features
            </a>
            <a
              className="text-on-surface-variant hover:text-white text-sm font-medium transition-colors"
              href="#work"
            >
              How it Works
            </a>
            <a
              className="text-on-surface-variant hover:text-white text-sm font-medium transition-colors"
              href="#pricing"
            >
              Pricing
            </a>
          </nav>
          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="px-5 h-10 flex items-center rounded-lg text-sm font-bold text-white hover:bg-surface-container-high transition-all"
            >
              Log In
            </Link>
            <Link
              to="/signup"
              className="px-6 h-10 flex items-center rounded-lg text-sm font-bold bg-linear-to-r from-primary to-secondary text-on-primary shadow-lg shadow-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      <main>
        {/* Hero Section */}
        <section className="relative pt-16 pb-20 px-6 overflow-hidden">
          <div className="absolute inset-0 hero-gradient"></div>
          <div
            className="absolute inset-0 opacity-[0.03]"
            style={{
              backgroundImage:
                "url('data:image/svg+xml,%3Csvg width=\\'60\\' height=\\'60\\' viewBox=\\'0 0 60 60\\' xmlns=\\'http://www.w3.org/2000/svg\\'%3E%3Cpath d=\\'M54.627 0l.83.828-1.415 1.415L51.8 0h2.827zM5.373 0l-.83.828L5.96 2.243 8.2 0H5.374zM48.97 0l3.83 3.83-1.414 1.414L46.143 0h2.828zM11.03 0L7.2 3.83 8.613 5.244 13.857 0h-2.828zM43.313 0l5.244 5.243-1.414 1.414L40.485 0h2.828zM16.687 0L11.443 5.243 12.857 6.657 19.515 0h-2.828zM37.657 0l6.657 6.657-1.414 1.414L34.83 0h2.827zM22.343 0L15.686 6.657 17.1 8.07 25.172 0h-2.83zM32 0l8.07 8.07-1.413 1.414L29.172 0H32zM28 0l-8.07 8.07 1.414 1.414L30.828 0H28z\\' fill=\\'%23ffffff\\' fillOpacity=\\'1\\' fillRule=\\'evenodd\\'/%3E%3C/svg%3E')",
            }}
          ></div>
          <div className="relative z-10 max-w-6xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10 mb-10">
              <span className="flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              <span className="text-[10px] font-black uppercase tracking-[0.25em] text-primary-fixed">
                v2.0 Next-Gen Platform
              </span>
            </div>
            <h1 className="text-5xl md:text-8xl font-black text-white leading-[1.05] tracking-tight mb-8">
              Automated QA, <br />
              <span className="text-gradient">Redefined by Intelligence</span>
            </h1>
            <p className="text-lg md:text-xl text-on-surface-variant/80 max-w-3xl mx-auto mb-12 leading-relaxed font-medium">
              WebSpector AI leverages advanced neural networks to eliminate
              regressions, audit performance, and guarantee API integrity. Built
              for the world's most demanding engineering teams.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-24">
              <Link
                to="/signup"
                className="w-full sm:w-auto px-10 h-14 rounded-full text-lg font-bold bg-linear-to-r from-primary to-secondary text-on-primary shadow-2xl shadow-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 flex items-center justify-center gap-3 group"
              >
                Get Started Free
                <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform">
                  arrow_forward
                </span>
              </Link>
              <button className="w-full sm:w-auto px-10 h-14 rounded-full text-lg font-bold text-white glass-panel hover:bg-white/10 transition-all flex items-center justify-center gap-2">
                View Technical Demo
              </button>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-32 px-6 bg-surface">
          <div className="max-w-7xl mx-auto">
            <div className="mb-24 max-w-3xl">
              <h2 className="text-primary text-sm font-bold uppercase tracking-widest mb-4">
                Core Capabilities
              </h2>
              <h3 className="text-4xl md:text-5xl font-bold text-white tracking-tight mb-6">
                Unmatched Precision for Modern Tech Stacks
              </h3>
              <p className="text-lg text-on-surface-variant leading-relaxed">
                Our suite of AI-driven tools provides comprehensive coverage for
                your modern web applications, eliminating blind spots in your
                development lifecycle.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Feature 1 */}
              <div className="group p-8 rounded-xl bg-surface-container hover:bg-surface-container-high transition-all duration-300 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 primary-gradient opacity-0 group-hover:opacity-10 blur-3xl transition-opacity"></div>
                <div className="w-14 h-14 rounded-lg bg-primary/10 flex items-center justify-center mb-8 border border-primary/20">
                  <span className="material-symbols-outlined text-primary text-3xl">
                    visibility
                  </span>
                </div>
                <h4 className="text-2xl font-bold text-white mb-4">
                  Visual Regression
                </h4>
                <p className="text-on-surface-variant leading-relaxed mb-6">
                  Pixel-perfect comparison powered by computer vision to catch
                  unintended UI changes across hundreds of browser/device
                  combinations.
                </p>
                <div className="h-1 w-0 group-hover:w-full primary-gradient transition-all duration-500 absolute bottom-0 left-0"></div>
              </div>
              {/* Feature 2 */}
              <div className="group p-8 rounded-xl bg-surface-container hover:bg-surface-container-high transition-all duration-300 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 primary-gradient opacity-0 group-hover:opacity-10 blur-3xl transition-opacity"></div>
                <div className="w-14 h-14 rounded-lg bg-secondary/10 flex items-center justify-center mb-8 border border-secondary/20">
                  <span className="material-symbols-outlined text-secondary text-3xl">
                    api
                  </span>
                </div>
                <h4 className="text-2xl font-bold text-white mb-4">
                  API Integrity
                </h4>
                <p className="text-on-surface-variant leading-relaxed mb-6">
                  Comprehensive schema validation and response monitoring to
                  keep your backend services reliable and your contracts
                  honored.
                </p>
                <div className="h-1 w-0 group-hover:w-full primary-gradient transition-all duration-500 absolute bottom-0 left-0"></div>
              </div>
              {/* Feature 3 */}
              <div className="group p-8 rounded-xl bg-surface-container hover:bg-surface-container-high transition-all duration-300 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 primary-gradient opacity-0 group-hover:opacity-10 blur-3xl transition-opacity"></div>
                <div className="w-14 h-14 rounded-lg bg-tertiary/10 flex items-center justify-center mb-8 border border-tertiary/20">
                  <span className="material-symbols-outlined text-tertiary text-3xl">
                    speed
                  </span>
                </div>
                <h4 className="text-2xl font-bold text-white mb-4">
                  Performance Audits
                </h4>
                <p className="text-on-surface-variant leading-relaxed mb-6">
                  Deep Lighthouse-based performance metrics captured
                  automatically on every deployment to ensure Core Web Vitals
                  remain optimized.
                </p>
                <div className="h-1 w-0 group-hover:w-full primary-gradient transition-all duration-500 absolute bottom-0 left-0"></div>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works Section - Redesigned */}
        <section
          id="work"
          className="py-32 px-6 bg-surface-container-lowest relative overflow-hidden"
        >
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full opacity-5 pointer-events-none">
            <div className="absolute inset-0 primary-gradient blur-[120px] rounded-full scale-150"></div>
          </div>
          <div className="max-w-7xl mx-auto relative z-10">
            <div className="text-center mb-24">
              <h2 className="text-4xl md:text-5xl font-black text-white mb-6 tracking-tight">
                Streamlined Intelligence
              </h2>
              <p className="text-on-surface-variant text-lg max-w-2xl mx-auto">
                Three steps to bulletproof software delivery, powered by our
                proprietary neural QA mesh.
              </p>
            </div>
            <div className="relative">
              {/* Linear Flow Connector */}
              <div className="hidden lg:block absolute top-24 left-0 w-full h-px bg-outline-variant/30 z-0"></div>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 relative z-10">
                {/* Step 1 */}
                <div className="group relative">
                  <div className="absolute -inset-2 bg-linear-to-b from-primary/20 to-transparent rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  <div className="relative glass-panel rounded-3xl p-8 h-full flex flex-col items-center text-center transition-transform duration-500 hover:-translate-y-2 border border-white/5">
                    <div className="w-16 h-16 rounded-2xl primary-gradient flex items-center justify-center mb-8 shadow-xl shadow-primary/20 relative">
                      <span className="material-symbols-outlined text-white text-3xl">
                        settings_input_component
                      </span>
                      <div className="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-surface-container-highest border border-white/10 flex items-center justify-center text-xs font-black text-primary">
                        01
                      </div>
                    </div>
                    <h4 className="text-2xl font-bold text-white mb-4">
                      Connect &amp; Deploy
                    </h4>
                    <p className="text-on-surface-variant leading-relaxed">
                      Seamlessly hook into your existing CI/CD pipelines.
                      WebSpector listens for deployment hooks to trigger instant
                      analysis.
                    </p>
                  </div>
                </div>
                {/* Step 2 */}
                <div className="group relative">
                  <div className="absolute -inset-2 bg-linear-to-b from-secondary/20 to-transparent rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  <div className="relative glass-panel rounded-3xl p-8 h-full flex flex-col items-center text-center transition-transform duration-500 hover:-translate-y-2 border border-white/5">
                    <div className="w-16 h-16 rounded-2xl bg-linear-to-br from-secondary to-primary-container flex items-center justify-center mb-8 shadow-xl shadow-secondary/20 relative">
                      <span className="material-symbols-outlined text-white text-3xl">
                        psychology
                      </span>
                      <div className="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-surface-container-highest border border-white/10 flex items-center justify-center text-xs font-black text-secondary">
                        02
                      </div>
                    </div>
                    <h4 className="text-2xl font-bold text-white mb-4">
                      AI Deep Scan
                    </h4>
                    <p className="text-on-surface-variant leading-relaxed">
                      Our autonomous agents crawl your application, simulating
                      real user behavior and stress-testing every API endpoint
                      in parallel.
                    </p>
                  </div>
                </div>
                {/* Step 3 */}
                <div className="group relative">
                  <div className="absolute -inset-2 bg-linear-to-b from-tertiary/20 to-transparent rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  <div className="relative glass-panel rounded-3xl p-8 h-full flex flex-col items-center text-center transition-transform duration-500 hover:-translate-y-2 border border-white/5">
                    <div className="w-16 h-16 rounded-2xl bg-linear-to-br from-tertiary to-secondary flex items-center justify-center mb-8 shadow-xl shadow-tertiary/20 relative">
                      <span className="material-symbols-outlined text-white text-3xl">
                        insights
                      </span>
                      <div className="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-surface-container-highest border border-white/10 flex items-center justify-center text-xs font-black text-tertiary">
                        03
                      </div>
                    </div>
                    <h4 className="text-2xl font-bold text-white mb-4">
                      Insights Delivered
                    </h4>
                    <p className="text-on-surface-variant leading-relaxed">
                      Receive comprehensive reports with prioritized bug fixes
                      and performance bottlenecks sent directly to Slack or
                      Microsoft Teams.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section id="pricing" className="py-32 px-6 bg-surface">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-20">
              <h2 className="text-4xl font-bold text-white mb-4">
                Simple, Scalable Pricing
              </h2>
              <p className="text-on-surface-variant">
                Choose the plan that fits your engineering team's scale.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Startup */}
              <div className="p-10 rounded-2xl bg-surface-container-low flex flex-col">
                <h4 className="text-lg font-bold text-on-surface-variant mb-2">
                  Startup
                </h4>
                <div className="flex items-baseline gap-1 mb-8">
                  <span className="text-5xl font-black text-white">$49</span>
                  <span className="text-on-surface-variant">/mo</span>
                </div>
                <ul className="space-y-4 mb-10 flex-grow">
                  <li className="flex items-center gap-3 text-sm">
                    <span className="material-symbols-outlined text-primary text-lg">
                      check_circle
                    </span>
                    5,000 AI Test Runs
                  </li>
                  <li className="flex items-center gap-3 text-sm">
                    <span className="material-symbols-outlined text-primary text-lg">
                      check_circle
                    </span>
                    Basic Visual Regression
                  </li>
                  <li className="flex items-center gap-3 text-sm">
                    <span className="material-symbols-outlined text-primary text-lg">
                      check_circle
                    </span>
                    2 Team Seats
                  </li>
                </ul>
                <button className="w-full py-4 rounded-lg border border-outline-variant text-white font-bold hover:bg-surface-container-high transition-all">
                  Get Started
                </button>
              </div>
              {/* Pro */}
              <div className="p-10 rounded-2xl bg-surface-container-high border border-primary/30 flex flex-col relative scale-105 shadow-2xl shadow-primary/10">
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full bg-linear-to-r from-primary to-secondary text-[10px] font-black uppercase tracking-[0.2em] text-on-primary">
                  Most Popular
                </div>
                <h4 className="text-lg font-bold text-primary mb-2">Pro</h4>
                <div className="flex items-baseline gap-1 mb-8">
                  <span className="text-5xl font-black text-white">$199</span>
                  <span className="text-on-surface-variant">/mo</span>
                </div>
                <ul className="space-y-4 mb-10 flex-grow">
                  <li className="flex items-center gap-3 text-sm">
                    <span
                      className="material-symbols-outlined text-primary text-lg"
                      style={{ fontVariationSettings: "'FILL' 1" }}
                    >
                      check_circle
                    </span>
                    50,000 AI Test Runs
                  </li>
                  <li className="flex items-center gap-3 text-sm">
                    <span
                      className="material-symbols-outlined text-primary text-lg"
                      style={{ fontVariationSettings: "'FILL' 1" }}
                    >
                      check_circle
                    </span>
                    Advanced Visual Regression
                  </li>
                  <li className="flex items-center gap-3 text-sm">
                    <span
                      className="material-symbols-outlined text-primary text-lg"
                      style={{ fontVariationSettings: "'FILL' 1" }}
                    >
                      check_circle
                    </span>
                    Unlimited API Monitoring
                  </li>
                  <li className="flex items-center gap-3 text-sm">
                    <span
                      className="material-symbols-outlined text-primary text-lg"
                      style={{ fontVariationSettings: "'FILL' 1" }}
                    >
                      check_circle
                    </span>
                    10 Team Seats
                  </li>
                </ul>
                <button className="w-full py-4 rounded-lg bg-linear-to-r from-primary to-secondary text-on-primary font-bold shadow-lg shadow-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300">
                  Start 14-Day Free Trial
                </button>
              </div>
              {/* Enterprise */}
              <div className="p-10 rounded-2xl bg-surface-container-low flex flex-col">
                <h4 className="text-lg font-bold text-on-surface-variant mb-2">
                  Enterprise
                </h4>
                <div className="flex items-baseline gap-1 mb-8">
                  <span className="text-4xl font-black text-white">Custom</span>
                </div>
                <ul className="space-y-4 mb-10 flex-grow">
                  <li className="flex items-center gap-3 text-sm text-on-surface-variant">
                    <span className="material-symbols-outlined text-primary text-lg">
                      check_circle
                    </span>
                    Unlimited Runs &amp; Seats
                  </li>
                  <li className="flex items-center gap-3 text-sm text-on-surface-variant">
                    <span className="material-symbols-outlined text-primary text-lg">
                      check_circle
                    </span>
                    On-Premise Deployment
                  </li>
                  <li className="flex items-center gap-3 text-sm text-on-surface-variant">
                    <span className="material-symbols-outlined text-primary text-lg">
                      check_circle
                    </span>
                    24/7 Dedicated Support
                  </li>
                  <li className="flex items-center gap-3 text-sm text-on-surface-variant">
                    <span className="material-symbols-outlined text-primary text-lg">
                      check_circle
                    </span>
                    Custom Integrations
                  </li>
                </ul>
                <button className="w-full py-4 rounded-lg border border-outline-variant text-white font-bold hover:bg-surface-container-high transition-all">
                  Contact Sales
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="py-32 px-6">
          <div className="max-w-5xl mx-auto relative rounded-3xl overflow-hidden">
            <div className="absolute inset-0 primary-gradient opacity-10"></div>
            <div className="relative z-10 px-8 py-24 md:px-20 text-center glass-panel border border-primary/20">
              <h2 className="text-4xl md:text-6xl font-black text-white mb-8 tracking-tight">
                Ready to ship with confidence?
              </h2>
              <p className="text-xl text-on-surface-variant mb-12 max-w-2xl mx-auto">
                Join 5,000+ engineering teams using WebSpector AI to automate
                their QA workflow.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
                <Link
                  to="/signup"
                  className="w-full sm:w-auto px-12 h-16 rounded-xl text-xl font-bold flex items-center justify-center bg-linear-to-r from-primary to-secondary text-on-primary shadow-2xl shadow-primary/40 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300"
                >
                  Start Your Free Trial
                </Link>
                <button className="w-full sm:w-auto px-12 h-16 rounded-xl text-xl font-bold flex items-center justify-center text-white bg-surface hover:bg-surface-container-high transition-all border border-outline-variant/30">
                  Schedule a Demo
                </button>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-surface-container-lowest border-t border-outline-variant/10 py-20 px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-12">
          <div className="col-span-2 md:col-span-1">
            <div className="flex items-center mb-6">
              <a
                href="#"
                className="text-2xl font-black tracking-tighter bg-linear-to-r from-primary to-secondary bg-clip-text text-transparent"
              >
                WebSpector
              </a>
            </div>
            <p className="text-sm text-on-surface-variant mb-8 leading-relaxed">
              The future of autonomous software quality assurance. Engineered
              for precision, delivered with intelligence.
            </p>
            <div className="flex gap-4">
              <a
                className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-on-surface-variant hover:text-white transition-colors"
                href="#"
              >
                <span className="material-symbols-outlined text-xl">
                  public
                </span>
              </a>
              <a
                className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-on-surface-variant hover:text-white transition-colors"
                href="#"
              >
                <span className="material-symbols-outlined text-xl">hub</span>
              </a>
            </div>
          </div>
          <div>
            <h5 className="text-white font-bold mb-6">Product</h5>
            <ul className="space-y-4 text-sm text-on-surface-variant">
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  Visual Regression
                </a>
              </li>
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  API Monitoring
                </a>
              </li>
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  Performance Audits
                </a>
              </li>
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  Integrations
                </a>
              </li>
            </ul>
          </div>
          <div>
            <h5 className="text-white font-bold mb-6">Company</h5>
            <ul className="space-y-4 text-sm text-on-surface-variant">
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  About Us
                </a>
              </li>
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  Careers
                </a>
              </li>
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  Security
                </a>
              </li>
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  Contact
                </a>
              </li>
            </ul>
          </div>
          <div>
            <h5 className="text-white font-bold mb-6">Legal</h5>
            <ul className="space-y-4 text-sm text-on-surface-variant">
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  Terms of Service
                </a>
              </li>
              <li>
                <a className="hover:text-primary transition-colors" href="#">
                  Cookie Policy
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="max-w-7xl mx-auto pt-20 mt-20 border-t border-outline-variant/10 flex flex-col md:flex-row justify-between items-center gap-6">
          <p className="text-xs text-on-surface-variant">
            © 2026 WebSpector AI. All rights reserved.
          </p>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-tertiary"></span>
            <span className="text-xs text-on-surface-variant">
              System Status: Operational
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
