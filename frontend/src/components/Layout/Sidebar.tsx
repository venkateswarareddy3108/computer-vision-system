import React from 'react';
import { Eye } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { Camera, Users, UserPlus, Activity } from 'lucide-react';

export const Sidebar = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <Eye size={28} />
        <span>VisionAnalytics</span>
      </div>
      <nav className="flex-col">
        <NavLink to="/dashboard" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
          <Camera size={20} />
          <span>Dashboard</span>
        </NavLink>
        <NavLink to="/register" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
          <UserPlus size={20} />
          <span>Registration</span>
        </NavLink>
        <NavLink to="/persons" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
          <Users size={20} />
          <span>Persons List</span>
        </NavLink>
        <NavLink to="/monitoring" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
          <Activity size={20} />
          <span>Monitoring</span>
        </NavLink>
      </nav>
    </aside>
  );
};
