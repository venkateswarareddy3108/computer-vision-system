import React from 'react';

export const Header = () => {
  return (
    <header className="topbar">
      <div className="flex items-center gap-md">
        <h1 style={{ fontSize: '1.125rem', fontWeight: 600 }}>Real-Time Computer Vision System</h1>
      </div>
      <div className="flex items-center gap-md">
        <span className="badge badge-success">System Online</span>
      </div>
    </header>
  );
};
