import React from 'react';
import Section from './ui/Section';
import { Star } from 'lucide-react';

const testimonials = [
  {
    name: "Alex Rivera",
    role: "Senior Frontend Dev",
    image: "https://picsum.photos/101/101",
    content: "The skill gap analysis was an eye-opener. I didn't realize I was missing key architectural concepts until BridgeIT pointed them out."
  },
  {
    name: "Marcus Chen",
    role: "Product Manager",
    image: "https://picsum.photos/102/102",
    content: "My mentor was fantastic. Being able to chat with someone who is actually in the role I wanted made all the difference."
  },
  {
    name: "Elena Rodriguez",
    role: "Data Scientist",
    image: "https://picsum.photos/103/103",
    content: "The roadmap feature kept me accountable. Seeing my progress bar fill up gave me the motivation to keep studying every night."
  }
];

const Testimonials: React.FC = () => {
  return (
    <Section className="bg-slate-900 text-white">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">Don't just take our word for it</h2>
        <p className="text-slate-400 text-lg">Join thousands of professionals who have accelerated their careers.</p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {testimonials.map((t, i) => (
          <div key={i} className="bg-slate-800/50 p-8 rounded-2xl border border-slate-700 hover:bg-slate-800 transition-colors">
            <div className="flex gap-1 mb-6">
              {[1,2,3,4,5].map(star => <Star key={star} size={16} className="fill-yellow-400 text-yellow-400" />)}
            </div>
            <p className="text-slate-300 mb-6 leading-relaxed">"{t.content}"</p>
            <div className="flex items-center gap-4">
              <img src={t.image} alt={t.name} className="w-12 h-12 rounded-full border-2 border-brand-500" />
              <div>
                <div className="font-bold">{t.name}</div>
                <div className="text-sm text-slate-400">{t.role}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Section>
  );
};

export default Testimonials;