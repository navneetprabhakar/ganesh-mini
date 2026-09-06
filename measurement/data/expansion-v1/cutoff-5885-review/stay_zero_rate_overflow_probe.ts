import { calculateStayQuote } from './solution';
let rejected = false;
try {
  calculateStayQuote({guestName: 'G', phone: 'P', adults: 1, children: 0,
    arrivalDay: -Number.MAX_VALUE, departureDay: Number.MAX_VALUE,
    units: [{id: 'free', nightlyRate: 0}], advance: 1, discount: 0});
} catch (error) { if (error instanceof RangeError) rejected = true; else throw error; }
if (!rejected) throw new Error('positive advance accepted for zero-rate stay through NaN subtotal');
