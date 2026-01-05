import React from "react";
import { Link } from "react-router-dom";
import { createPageUrl } from "./utils";
import { FileCheck, Upload, History, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button.jsx";

export default function Layout({ children, currentPageName }) {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);

  const navItems = [
    { name: "Validar", page: "Home", icon: Upload },
    { name: "Histórico", page: "History", icon: History },
  ];

  return (
    <div className="min-h-screen">
      {/* Mobile Header */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-2xl border-b border-slate-200/60 px-4 py-3.5 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-gradient-to-br from-blue-600 via-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25 transition-transform hover:scale-105">
              <FileCheck className="w-5 h-5 text-white" />
            </div>
            <span className="font-semibold text-slate-800 tracking-tight">Validador</span>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="rounded-xl hover:bg-slate-100"
          >
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </Button>
        </div>
      </div>

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 h-full w-72 bg-white/80 backdrop-blur-2xl border-r border-slate-200/60 z-40 transform transition-all duration-300 ease-out lg:translate-x-0 shadow-xl ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        <div className="p-6 h-full flex flex-col">
          <div className="flex items-center gap-3 mb-12">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 via-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-xl shadow-blue-500/30 transition-transform hover:scale-105 cursor-pointer">
              <FileCheck className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-slate-900 text-xl tracking-tight">Validador</h1>
              <p className="text-xs text-slate-500 font-medium">de Documentos</p>
            </div>
          </div>

          <nav className="space-y-2 flex-1">
            {navItems.map((item, index) => {
              const isActive = currentPageName === item.page;
              return (
                <Link
                  key={item.page}
                  to={createPageUrl(item.page)}
                  onClick={() => setSidebarOpen(false)}
                  className={`flex items-center gap-3.5 px-4 py-3.5 rounded-xl transition-all duration-300 group relative overflow-hidden ${
                    isActive
                      ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/30 scale-[1.02]"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900 hover:scale-[1.01]"
                  }`}
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  {isActive && (
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-indigo-600/20 animate-pulse" />
                  )}
                  <item.icon className={`w-5 h-5 relative z-10 transition-transform ${isActive ? "text-white" : "text-slate-400 group-hover:text-blue-600 group-hover:scale-110"}`} />
                  <span className="font-medium relative z-10">{item.name}</span>
                  {isActive && (
                    <div className="absolute right-3 w-1.5 h-1.5 bg-white rounded-full animate-pulse" />
                  )}
                </Link>
              );
            })}
          </nav>

          <div className="mt-auto pt-6">
            <div className="bg-gradient-to-br from-slate-50/80 to-slate-100/80 backdrop-blur-sm rounded-2xl p-4 border border-slate-200/60 shadow-sm">
              <p className="text-xs text-slate-500 mb-1 font-medium">Versão</p>
              <p className="text-sm font-semibold text-slate-700">1.0.0 Beta</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/30 backdrop-blur-sm z-30 lg:hidden transition-opacity duration-300"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <main className="lg:ml-72 min-h-screen pt-16 lg:pt-0">
        <div className="p-6 lg:p-10 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}

