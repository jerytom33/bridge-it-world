import React from 'react';
import Section from './ui/Section';
import { Search, Map, Rocket } from 'lucide-react';

const steps = [
  {
    id: '01',
    title: 'Assess Your Profile',
    desc: 'Upload your CV or link your LinkedIn. Our AI analyzes your experience and identifies key strengths.',
    icon: <Search className="w-6 h-6 text-white" />,
    color: 'bg-brand-500'
  },
  {
    id: '02',
    title: 'Define Your Goal',
    desc: 'Tell us where you want to be. Senior Engineer? Product Manager? We map the route.',
    icon: <Map className="w-6 h-6 text-white" />,
    color: 'bg-accent-500'
  },
  {
    id: '03',
    title: 'Bridge the Gap',
    desc: 'Execute your custom plan with courses, projects, and mentorship until you land the role.',
    icon: <Rocket className="w-6 h-6 text-white" />,
    color: 'bg-teal-500'
  }
];

const HowItWorks: React.FC = () => {
  return (
    <Section id="how-it-works">
      <div className="grid lg:grid-cols-2 gap-16 items-center">
        <div>
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-6">
            Your journey to success, <br />
            <span className="text-gradient">simplified.</span>
          </h2>
          <p className="text-lg text-slate-600 mb-12">
            Career growth shouldn't be a mystery. We've broken it down into a science.
            Follow our proven framework to achieve your professional dreams.
          </p>

          <div className="space-y-10 relative">
            {/* Connecting Line */}
            <div className="absolute left-6 top-6 bottom-6 w-0.5 bg-slate-100 -z-10" />

            {steps.map((step) => (
              <div key={step.id} className="flex gap-6">
                <div className={`relative shrink-0 w-12 h-12 rounded-full ${step.color} shadow-lg shadow-brand-500/20 flex items-center justify-center ring-4 ring-white`}>
                  {step.icon}
                </div>
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-sm font-bold text-slate-400 tracking-wider">STEP {step.id}</span>
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">{step.title}</h3>
                  <p className="text-slate-600">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-tr from-brand-100 to-accent-100 rounded-3xl transform rotate-3 scale-105 opacity-50" />
          <img 
            src="https://picsum.photos/600/600" 
            alt="Career planning session" 
            className="relative rounded-3xl shadow-2xl object-cover w-full h-auto aspect-square hover:rotate-0 transition-transform duration-500"
          />
          
          {/* Floater */}
          <div className="absolute -bottom-6 -left-6 bg-white p-6 rounded-xl shadow-xl max-w-xs">
            <div className="flex items-center gap-4 mb-3">
              <div className="w-10 h-10 rounded-full bg-slate-200 overflow-hidden">
                 <img src="https://picsum.photos/100/100" alt="User" />
              </div>
              <div>
                <div className="font-bold text-slate-900">Sarah J.</div>
                <div className="text-xs text-green-600 font-medium">Just landed a job!</div>
              </div>
            </div>
            <p className="text-sm text-slate-600 italic">"BridgeIT helped me pivot from Sales to UX Design in just 6 months!"</p>
          </div>
        </div>
      </div>
    </Section>
  );
};

export default HowItWorks;