import React from 'react';
import { createRoot } from 'react-dom/client';
import Strands from './components/Strands.jsx';
import BookingWizard from './components/BookingWizard.jsx';

function BookingPage({ services, csrfToken, formErrors, formData }) {
  return (
    <>
      <Strands
        style={{ position: 'absolute', inset: 0 }}
        colors={['#002b5b', '#00decf', '#7594ca', '#ffe16d']}
        count={4}
        speed={0.4}
        amplitude={0.7}
        waviness={0.9}
        thickness={0.5}
        glow={1.8}
        taper={2.5}
        spread={1}
        intensity={0.45}
        saturation={1.2}
        opacity={0.35}
        scale={1.4}
      />
      <div className="app-shell relative z-10 max-w-5xl">
        <BookingWizard
          services={services}
          csrfToken={csrfToken}
          formErrors={formErrors}
          formData={formData}
        />
      </div>
    </>
  );
}

const mount = document.getElementById('booking-app');
if (mount) {
  let services = [];
  let formErrors = {};
  let formData = {};
  try {
    services = JSON.parse(mount.dataset.services || '[]');
  } catch {
    services = [];
  }
  try {
    formErrors = JSON.parse(mount.dataset.formErrors || '{}');
  } catch {
    formErrors = {};
  }
  try {
    formData = JSON.parse(mount.dataset.formData || '{}');
  } catch {
    formData = {};
  }
  createRoot(mount).render(
    <BookingPage
      services={services}
      csrfToken={mount.dataset.csrf || ''}
      formErrors={formErrors}
      formData={formData}
    />
  );
}
