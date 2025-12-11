import React from 'react';
import { Target, UserCheck, BrainCircuit, LineChart, Briefcase, MessageSquare } from 'lucide-react';
import Section from './ui/Section';

const features = [
  {
    icon: <BrainCircuit size={24} />,
    title: "AI Skill Analysis",
    description: "Our advanced AI evaluates your current skill set against industry standards to identify gaps instantly.",
    color: "text-brand-600",
    bg: "bg-brand-50"
  },
  {
    icon: <Target size={24} />,
    title: "Personalized Roadmap",
    description: "Get a custom step-by-step plan tailored to your career goals, timeline, and learning style.",
    color: "text-accent-600",
    bg: "bg-accent-50"
  },
  {
    icon: <UserCheck size={24} />,
    title: "Expert Mentorship",
    description: "Connect with industry leaders who have walked your path and can guide you around obstacles.",
    color: "text-teal-600",
    bg: "bg-teal-50"
  },
  {
    icon: <LineChart size={24} />,
    title: "Progress Tracking",
    description: "Visualize your growth with dynamic dashboards that track certifications, projects, and soft skills.",
    color: "text-amber-600",
    bg: "bg-amber-50"
  },
  {
    icon: <Briefcase size={24} />,
    title: "Job Matching",
    description: "Access a curated list of job openings that perfectly match your newly acquired skills.",
    color: "text-rose-600",
    bg: "bg-rose-50"
  },
  {
    icon: <MessageSquare size={24} />,
    title: "Mock Interviews",
    description: "Practice with AI-driven interview simulations that give real-time feedback on your answers.",
    color: "text-indigo-600",
    bg: "bg-indigo-50"
  }
];

const Features: React.FC = () => {
  return (
    <Section id="features" className="bg-slate-50/50">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
          Everything you need to <span className="text-gradient">level up</span>
        </h2>
        <p className="text-slate-600 text-lg">
          We combine cutting-edge technology with human expertise to provide the most comprehensive career guidance platform available.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {features.map((feature, index) => (
          <div 
            key={index}
            className="group p-8 bg-white rounded-2xl shadow-sm border border-slate-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
          >
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-6 ${feature.bg} ${feature.color} group-hover:scale-110 transition-transform`}>
              {feature.icon}
            </div>
            <h3 className="text-xl font-bold text-slate-900 mb-3">{feature.title}</h3>
            <p className="text-slate-600 leading-relaxed">{feature.description}</p>
          </div>
        ))}
      </div>
    </Section>
  );
};

export default Features;