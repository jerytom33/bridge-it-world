import React from 'react';
import { Compass, Twitter, Linkedin, Github, Heart } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-100 pt-16 pb-8">
      <div className="container mx-auto px-4 md:px-6">
        <div className="grid md:grid-cols-4 gap-12 mb-12">
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="bg-brand-600 p-1.5 rounded text-white">
                <Compass size={20} />
              </div>
              <span className="text-xl font-bold text-slate-900">BridgeIT</span>
            </div>
            <p className="text-slate-500 text-sm leading-relaxed">
              Empowering professionals to navigate their career paths with data-driven insights and human connection.
            </p>
            <div className="flex gap-4 pt-2">
              <a href="#" className="text-slate-400 hover:text-brand-600 transition-colors"><Twitter size={20} /></a>
              <a href="#" className="text-slate-400 hover:text-brand-600 transition-colors"><Linkedin size={20} /></a>
              <a href="#" className="text-slate-400 hover:text-brand-600 transition-colors"><Github size={20} /></a>
            </div>
          </div>

          <div>
            <h4 className="font-bold text-slate-900 mb-4">Platform</h4>
            <ul className="space-y-2 text-sm text-slate-600">
              <li><a href="#" className="hover:text-brand-600">Features</a></li>
              <li><a href="#" className="hover:text-brand-600">How it Works</a></li>
              <li><a href="#" className="hover:text-brand-600">Pricing</a></li>
              <li><a href="#" className="hover:text-brand-600">Enterprise</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-slate-900 mb-4">Resources</h4>
            <ul className="space-y-2 text-sm text-slate-600">
              <li><a href="#" className="hover:text-brand-600">Blog</a></li>
              <li><a href="#" className="hover:text-brand-600">Career Guides</a></li>
              <li><a href="#" className="hover:text-brand-600">Salary Calculator</a></li>
              <li><a href="#" className="hover:text-brand-600">Help Center</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-slate-900 mb-4">Legal</h4>
            <ul className="space-y-2 text-sm text-slate-600">
              <li><a href="#" className="hover:text-brand-600">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-brand-600">Terms of Service</a></li>
              <li><a href="#" className="hover:text-brand-600">Cookie Policy</a></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-100 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-slate-500">
            © {new Date().getFullYear()} BridgeIT Inc. All rights reserved.
          </p>
          <div className="flex items-center gap-1 text-sm text-slate-500">
            Made with <Heart size={14} className="fill-red-500 text-red-500" /> for ambitious careers.
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;