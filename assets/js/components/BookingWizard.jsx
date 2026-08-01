import React, { useState } from 'react';

const TOTAL_STEPS = 4;

const STEP_META = {
  1: { title: 'Choisir le service', desc: 'Sélectionnez votre formule', progress: 25 },
  2: { title: 'Date et heure', desc: 'Choisissez votre créneau', progress: 50 },
  3: { title: 'Vos informations', desc: 'Nom et téléphone', progress: 75 },
  4: { title: 'Confirmation', desc: 'Vérifiez et confirmez', progress: 100 },
};

const TIME_SLOTS = ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'];

const SERVICE_ICONS = ['speed', 'auto_fix_high', 'diamond'];

function formatPrice(price) {
  const n = Number(price);
  return Number.isInteger(n) ? `${n} DT` : `${n.toFixed(2)} DT`;
}

export default function BookingWizard({ services = [], csrfToken = '' }) {
  const [step, setStep] = useState(1);
  const [service, setService] = useState(services[0]?.name ?? '');
  const [date, setDate] = useState('');
  const [time, setTime] = useState('08:00');
  const [customerName, setCustomerName] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [notes, setNotes] = useState('');

  const meta = STEP_META[step];
  const isLastStep = step === TOTAL_STEPS;

  const canNext = () => {
    if (step === 1) return service !== '';
    if (step === 2) return date !== '' && time !== '';
    if (step === 3) return customerName.trim() !== '' && customerPhone.trim() !== '';
    return true;
  };

  const handleNext = (e) => {
    if (step < TOTAL_STEPS) {
      e.preventDefault();
      setStep(step + 1);
    }
  };

  const stepCls = 'step-transition';
  const inputCls =
    'w-full px-md py-sm rounded-xl border border-outline-variant bg-surface-container-lowest focus:ring-2 focus:ring-secondary/30 focus:border-secondary outline-none transition-all text-body-md';

  return (
    <>
      <div className="mb-lg">
        <div className="flex justify-between items-end mb-sm">
          <div>
            <span className="text-label-sm uppercase tracking-widest text-primary/60">
              Étape {step} sur {TOTAL_STEPS}
            </span>
            <h1 className="text-headline-lg text-primary font-bold">{meta.title}</h1>
          </div>
          <div className="text-right hidden sm:block">
            <span className="text-body-md text-on-surface-variant">{meta.desc}</span>
          </div>
        </div>
        <div className="h-2 w-full bg-surface-container-highest rounded-full overflow-hidden">
          <div
            className="h-full progress-gradient step-transition"
            style={{ width: `${meta.progress}%` }}
          />
        </div>
      </div>

      <form id="booking-form" method="POST" action="/bookings/new/" onSubmit={handleNext} className="relative overflow-hidden min-h-[450px]">
        {csrfToken && <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />}

        {step === 1 && (
          <div key="step-1" className={stepCls}>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-md">
              {services.map((s, i) => (
                <label key={s.name} className="group relative cursor-pointer">
                  <input
                    type="radio"
                    name="service"
                    value={s.name}
                    className="peer sr-only"
                    checked={service === s.name}
                    onChange={() => setService(s.name)}
                  />
                  <div className="p-lg rounded-xl bg-surface-container-lowest border border-outline-variant/30 peer-checked:border-secondary peer-checked:ring-2 peer-checked:ring-secondary/20 shadow-sm transition-all hover:shadow-md h-full flex flex-col">
                    <div className="w-12 h-12 rounded-full bg-primary/5 flex items-center justify-center mb-md group-hover:scale-110 transition-transform">
                      <span className="material-symbols-outlined text-primary text-3xl">
                        {SERVICE_ICONS[i] || 'local_car_wash'}
                      </span>
                    </div>
                    <h3 className="text-headline-md mb-xs">{s.name}</h3>
                    <p className="text-body-md text-on-surface-variant mb-md flex-grow">{s.description}</p>
                    <div className="flex justify-between items-center mt-auto">
                      <span className="text-headline-md font-bold text-primary">{formatPrice(s.price)}</span>
                      <span className="text-label-sm text-secondary font-bold uppercase">{s.duration_minutes} min</span>
                    </div>
                  </div>
                </label>
              ))}
              {services.length === 0 && (
                <p className="text-body-md text-on-surface-variant">Aucun service disponible pour le moment.</p>
              )}
            </div>
          </div>
        )}

        {step === 2 && (
          <div key="step-2" className={stepCls}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-lg">
              <div>
                <label className="text-label-md text-primary block mb-md" htmlFor="booking-date">
                  Date
                </label>
                <input
                  id="booking-date"
                  aria-required="true"
                  type="date"
                  name="date"
                  required
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className={inputCls}
                />
              </div>
              <div>
                <label className="text-label-md text-primary block mb-md">Heure</label>
                <div className="grid grid-cols-2 gap-sm">
                  {TIME_SLOTS.map((slot) => (
                    <label key={slot} className="cursor-pointer">
                      <input
                        required
                        type="radio"
                        name="time"
                        value={slot}
                        className="peer sr-only"
                        checked={time === slot}
                        onChange={() => setTime(slot)}
                      />
                      <div className="py-sm px-md text-center rounded-xl border border-outline-variant/30 bg-surface-container-lowest peer-checked:bg-primary-container peer-checked:text-on-primary-container peer-checked:border-primary-container transition-all text-body-md">
                        {slot}
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {step === 3 && (
          <div key="step-3" className={stepCls}>
            <div className="space-y-lg max-w-lg mx-auto">
              <div className="space-y-xs">
                <label className="text-label-md text-primary" htmlFor="customer_name">
                  Nom complet
                </label>
                <input
                  id="customer_name"
                  required
                  type="text"
                  name="customer_name"
                  placeholder="Votre nom"
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  className={inputCls}
                />
              </div>
              <div className="space-y-xs">
                <label className="text-label-md text-primary" htmlFor="customer_phone">
                  Téléphone
                </label>
                <input
                  id="customer_phone"
                  required
                  type="tel"
                  name="customer_phone"
                  placeholder="Votre numéro"
                  value={customerPhone}
                  onChange={(e) => setCustomerPhone(e.target.value)}
                  className={inputCls}
                />
              </div>
              <div className="space-y-xs">
                <label className="text-label-md text-primary" htmlFor="notes">
                  Notes (optionnel)
                </label>
                <textarea
                  id="notes"
                  name="notes"
                  rows="3"
                  placeholder="Demandes particulières..."
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className={inputCls}
                />
              </div>
            </div>
          </div>
        )}

        {step === 4 && (
          <div key="step-4" className={stepCls}>
            <div className="max-w-lg mx-auto">
              <div className="glass-card p-lg rounded-2xl border border-secondary/20 shadow-xl shadow-primary/5">
                <h4 className="text-label-md text-secondary uppercase tracking-widest mb-md">Récapitulatif</h4>
                <div className="space-y-sm">
                  <div className="flex justify-between py-xs border-b border-outline-variant/10">
                    <span className="text-on-surface-variant text-body-md">Service</span>
                    <span className="text-primary font-bold">{service || '—'}</span>
                  </div>
                  <div className="flex justify-between py-xs border-b border-outline-variant/10">
                    <span className="text-on-surface-variant text-body-md">Date</span>
                    <span className="text-primary font-bold">{date || '—'}</span>
                  </div>
                  <div className="flex justify-between py-xs border-b border-outline-variant/10">
                    <span className="text-on-surface-variant text-body-md">Heure</span>
                    <span className="text-primary font-bold">{time || '—'}</span>
                  </div>
                  <div className="flex justify-between py-xs border-b border-outline-variant/10">
                    <span className="text-on-surface-variant text-body-md">Client</span>
                    <span className="text-primary font-bold">{customerName || '—'}</span>
                  </div>
                  <div className="flex justify-between py-xs">
                    <span className="text-on-surface-variant text-body-md">Téléphone</span>
                    <span className="text-primary font-bold">{customerPhone || '—'}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </form>

      <div className="mt-lg flex justify-between items-center">
        {step > 1 ? (
          <button
            type="button"
            onClick={() => setStep(step - 1)}
            className="flex items-center gap-xs font-label-md text-on-surface-variant hover:text-primary transition-colors px-md py-sm rounded-full"
          >
            <span className="material-symbols-outlined">arrow_back</span>
            Retour
          </button>
        ) : (
          <span />
        )}
        <div className="flex-grow" />
        <button
          type="submit"
          form="booking-form"
          disabled={!canNext()}
          className="bg-primary text-on-primary px-lg py-sm rounded-full font-label-md hover:shadow-lg active:scale-95 transition-all flex items-center gap-xs disabled:opacity-40 disabled:cursor-not-allowed disabled:active:scale-100"
        >
          {isLastStep ? 'Confirmer la réservation' : 'Continuer'}
          <span className="material-symbols-outlined">{isLastStep ? 'check_circle' : 'arrow_forward'}</span>
        </button>
      </div>
    </>
  );
}
