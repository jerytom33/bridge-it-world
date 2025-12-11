import React from 'react';
import { Play, TrendingUp, Users, Award } from 'lucide-react';
import Button from './ui/Button';
import Section from './ui/Section';

const Hero: React.FC = () => {
  return (
    <Section className="pt-32 pb-16 lg:pt-48 lg:pb-32">
      {/* Background Decor */}
      <div className="absolute top-0 right-0 -z-10 w-full h-full overflow-hidden opacity-30 pointer-events-none">
         <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-brand-400 rounded-full blur-[100px] opacity-20 animate-pulse" />
         <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-accent-400 rounded-full blur-[100px] opacity-20" />
      </div>

      <div className="grid lg:grid-cols-2 gap-12 items-center">
        {/* Text Content */}
        <div className="space-y-8 text-center lg:text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 border border-brand-100 text-brand-700 text-sm font-medium mx-auto lg:mx-0">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-500"></span>
            </span>
            New: AI Resume Analysis Feature
          </div>

          <h1 className="text-5xl lg:text-7xl font-extrabold tracking-tight text-slate-900 leading-[1.1]">
            Bridge the gap to your <br className="hidden lg:block" />
            <span className="text-gradient">Dream Career</span>
          </h1>
          
          <p className="text-lg text-slate-600 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
            Stop guessing your next move. BridgeIT uses advanced AI to analyze your skills, 
            match you with expert mentors, and build a personalized roadmap to success.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
            <Button size="lg" withArrow>Start Your Journey</Button>
            <button className="flex items-center gap-3 px-6 py-4 rounded-full text-slate-700 font-semibold hover:bg-slate-50 transition-colors">
              <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-brand-600">
                <Play fill="currentColor" size={16} />
              </div>
              Watch Demo
            </button>
          </div>

          <div className="pt-8 flex items-center justify-center lg:justify-start gap-8 text-slate-500">
            <div className="flex items-center gap-2">
              <Users size={20} />
              <span className="text-sm font-medium">10k+ Users</span>
            </div>
            <div className="flex items-center gap-2">
              <Award size={20} />
              <span className="text-sm font-medium">Top Rated</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp size={20} />
              <span className="text-sm font-medium">95% Success</span>
            </div>
          </div>
        </div>

        {/* Visual Content */}
        <div className="relative mx-auto w-full max-w-[600px] lg:max-w-none">
          <div className="relative z-10 bg-white rounded-2xl shadow-2xl shadow-brand-900/10 border border-slate-100 overflow-hidden transform hover:scale-[1.02] transition-transform duration-500">
            {/* Mock Dashboard Header */}
            <div className="bg-slate-50 border-b border-slate-100 p-4 flex items-center gap-4">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-400" />
                <div className="w-3 h-3 rounded-full bg-amber-400" />
                <div className="w-3 h-3 rounded-full bg-green-400" />
              </div>
              <div className="h-2 w-32 bg-slate-200 rounded-full" />
            </div>
            
            {/* Mock Dashboard Body */}
            <div className="p-6 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <div className="h-4 w-48 bg-slate-200 rounded mb-2" />
                  <div className="h-3 w-32 bg-slate-100 rounded" />
                </div>
                <div className="h-10 w-10 rounded-full bg-brand-100 flex items-center justify-center text-brand-600 font-bold">
                  92%
                </div>
              </div>

              {/* Progress Bars */}
              <div className="space-y-4">
                {[
                  { label: "Technical Skills", val: "w-[85%]", color: "bg-brand-500" },
                  { label: "Soft Skills", val: "w-[65%]", color: "bg-accent-500" },
                  { label: "Leadership", val: "w-[40%]", color: "bg-teal-400" }
                ].map((item, idx) => (
                  <div key={idx} className="space-y-2">
                    <div className="flex justify-between text-xs font-semibold text-slate-500">
                      <span>{item.label}</span>
                    </div>
                    <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div className={`h-full ${item.color} ${item.val} rounded-full`} />
                    </div>
                  </div>
                ))}
              </div>

              {/* Recommendation Card */}
              <div className="bg-brand-50 rounded-xl p-4 flex gap-4 items-start">
                <div className="p-2 bg-white rounded-lg shadow-sm text-brand-600">
                   <TrendingUp size={20} />
                </div>
                <div>
                   <div className="text-sm font-bold text-slate-800">Recommended Path</div>
                   <div className="text-xs text-slate-600 mt-1">Based on your gap analysis, consider the Senior React Developer certification track.</div>
                </div>
              </div>
            </div>
          </div>

          {/* Floating Cards */}
          <div className="absolute -left-12 bottom-12 z-20 bg-white p-4 rounded-xl shadow-xl border border-slate-100 hidden lg:flex items-center gap-3 animate-bounce" style={{ animationDuration: '3s' }}>
             <div className="h-10 w-10 rounded-full bg-green-100 flex items-center justify-center text-green-600">
                <Award size={20} />
             </div>
             <div>
                <div className="text-xs text-slate-500">New Achievement</div>
                <div className="text-sm font-bold text-slate-800">Fast Learner</div>
             </div>
          </div>
        </div>
      </div>
    </Section>
  );
};

export default Hero;