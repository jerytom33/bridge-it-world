import React from 'react';
import Section from './ui/Section';
import Button from './ui/Button';

const CtaSection: React.FC = () => {
  return (
    <Section className="py-24">
      <div className="bg-gradient-to-r from-brand-600 to-accent-600 rounded-3xl p-8 md:p-16 text-center text-white relative overflow-hidden shadow-2xl">
        {/* Abstract Background Shapes */}
        <div className="absolute top-0 left-0 w-64 h-64 bg-white opacity-10 rounded-full blur-3xl transform -translate-x-1/2 -translate-y-1/2" />
        <div className="absolute bottom-0 right-0 w-64 h-64 bg-black opacity-10 rounded-full blur-3xl transform translate-x-1/2 translate-y-1/2" />
        
        <div className="relative z-10 max-w-2xl mx-auto space-y-8">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
            Ready to build your bridge?
          </h2>
          <p className="text-brand-100 text-lg md:text-xl">
            Join BridgeIT today and take the first step towards the career you deserve. 
            No credit card required for the initial assessment.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Button size="lg" className="bg-white text-brand-600 hover:bg-brand-50 hover:text-brand-700 shadow-none">
              Get Started for Free
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/10 focus:ring-white">
              View Pricing Plans
            </Button>
          </div>
        </div>
      </div>
    </Section>
  );
};

export default CtaSection;