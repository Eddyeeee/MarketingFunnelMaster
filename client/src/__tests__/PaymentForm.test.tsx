import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { PaymentForm } from '../components/PaymentForm';
import { useToast } from '../hooks/use-toast';
import { useAnalytics } from '../hooks/use-analytics';

// Mock hooks
vi.mock('../hooks/use-toast');
vi.mock('../hooks/use-analytics');

// Mock fetch
global.fetch = vi.fn();

const mockToast = {
  toast: vi.fn()
};

const mockAnalytics = {
  trackEvent: vi.fn()
};

(useToast as any).mockReturnValue(mockToast);
(useAnalytics as any).mockReturnValue(mockAnalytics);

describe('PaymentForm', () => {
  const defaultProps = {
    personaType: 'student',
    leadId: 123,
    leadData: {
      email: 'test@example.com',
      firstName: 'Max',
      lastName: 'Mustermann'
    },
    onSuccess: vi.fn(),
    onError: vi.fn()
  };

  beforeEach(() => {
    vi.clearAllMocks();
    (fetch as any).mockClear();
  });

  it('renders payment form with product selection', async () => {
    const mockProducts = [
      {
        id: 'student_basic',
        name: 'Student Magic Tool Basic',
        description: 'Perfekt für Studenten',
        price: 97,
        currency: 'eur',
        features: ['Magic Tool Zugang', 'Studenten-Strategien'],
        bonusItems: ['Studenten-Bonus-Guide', '500€-Challenge']
      }
    ];

    const mockPaymentMethods = [
      {
        id: 'card',
        name: 'Kreditkarte',
        description: 'Visa, Mastercard, American Express',
        icon: '💳',
        enabled: true
      }
    ];

    (fetch as any)
      .mockResolvedValueOnce({
        json: async () => ({ success: true, products: mockProducts })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentMethods: mockPaymentMethods })
      });

    render(<PaymentForm {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('🎯 Wähle dein Magic Tool Paket')).toBeInTheDocument();
    });

    expect(screen.getByText('Student Magic Tool Basic')).toBeInTheDocument();
    expect(screen.getByText('💳 Zahlungsmethode wählen')).toBeInTheDocument();
  });

  it('loads products and payment methods on mount', async () => {
    const mockProducts = [
      {
        id: 'student_basic',
        name: 'Student Magic Tool Basic',
        price: 97,
        currency: 'eur',
        features: [],
        bonusItems: []
      }
    ];

    const mockPaymentMethods = [
      {
        id: 'card',
        name: 'Kreditkarte',
        description: 'Visa, Mastercard, American Express',
        icon: '💳',
        enabled: true
      }
    ];

    (fetch as any)
      .mockResolvedValueOnce({
        json: async () => ({ success: true, products: mockProducts })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentMethods: mockPaymentMethods })
      });

    render(<PaymentForm {...defaultProps} />);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/payment/products/student');
      expect(fetch).toHaveBeenCalledWith('/api/payment/payment-methods');
    });
  });

  it('creates payment intent when card payment is selected', async () => {
    const mockProducts = [
      {
        id: 'student_basic',
        name: 'Student Magic Tool Basic',
        price: 97,
        currency: 'eur',
        features: [],
        bonusItems: []
      }
    ];

    const mockPaymentMethods = [
      {
        id: 'card',
        name: 'Kreditkarte',
        description: 'Visa, Mastercard, American Express',
        icon: '💳',
        enabled: true
      }
    ];

    const mockPaymentIntent = {
      id: 'pi_test123',
      clientSecret: 'pi_test123_secret_abc',
      status: 'requires_payment_method'
    };

    (fetch as any)
      .mockResolvedValueOnce({
        json: async () => ({ success: true, products: mockProducts })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentMethods: mockPaymentMethods })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentIntent: mockPaymentIntent })
      });

    render(<PaymentForm {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('Student Magic Tool Basic')).toBeInTheDocument();
    });

    const paymentButton = screen.getByText('🚀 Jetzt kaufen & sofort starten!');
    fireEvent.click(paymentButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/payment/create-payment-intent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          amount: 97,
          currency: 'eur',
          personaType: 'student',
          leadId: 123,
          email: 'test@example.com',
          firstName: 'Max',
          lastName: 'Mustermann',
          paymentMethod: 'card',
          metadata: {
            productId: 'student_basic',
            personaType: 'student'
          }
        })
      });
    });
  });

  it('creates checkout session for non-card payment methods', async () => {
    const mockProducts = [
      {
        id: 'student_basic',
        name: 'Student Magic Tool Basic',
        price: 97,
        currency: 'eur',
        features: [],
        bonusItems: []
      }
    ];

    const mockPaymentMethods = [
      {
        id: 'sepa',
        name: 'SEPA-Lastschrift',
        description: 'Direkte Abbuchung vom Konto',
        icon: '🏦',
        enabled: true
      }
    ];

    const mockCheckoutUrl = 'https://checkout.stripe.com/test';

    (fetch as any)
      .mockResolvedValueOnce({
        json: async () => ({ success: true, products: mockProducts })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentMethods: mockPaymentMethods })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, checkoutUrl: mockCheckoutUrl })
      });

    // Mock window.location.href
    Object.defineProperty(window, 'location', {
      value: { href: '' },
      writable: true
    });

    render(<PaymentForm {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('Student Magic Tool Basic')).toBeInTheDocument();
    });

    // Select SEPA payment method
    const sepaMethod = screen.getByText('SEPA-Lastschrift');
    fireEvent.click(sepaMethod);

    const paymentButton = screen.getByText('🚀 Jetzt kaufen & sofort starten!');
    fireEvent.click(paymentButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/payment/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          amount: 97,
          currency: 'eur',
          personaType: 'student',
          leadId: 123,
          email: 'test@example.com',
          firstName: 'Max',
          lastName: 'Mustermann',
          paymentMethod: 'sepa',
          metadata: {
            productId: 'student_basic',
            personaType: 'student'
          }
        })
      });
    });
  });

  it('shows error toast when payment creation fails', async () => {
    const mockProducts = [
      {
        id: 'student_basic',
        name: 'Student Magic Tool Basic',
        price: 97,
        currency: 'eur',
        features: [],
        bonusItems: []
      }
    ];

    const mockPaymentMethods = [
      {
        id: 'card',
        name: 'Kreditkarte',
        description: 'Visa, Mastercard, American Express',
        icon: '💳',
        enabled: true
      }
    ];

    (fetch as any)
      .mockResolvedValueOnce({
        json: async () => ({ success: true, products: mockProducts })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentMethods: mockPaymentMethods })
      })
      .mockRejectedValueOnce(new Error('Payment failed'));

    render(<PaymentForm {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('Student Magic Tool Basic')).toBeInTheDocument();
    });

    const paymentButton = screen.getByText('🚀 Jetzt kaufen & sofort starten!');
    fireEvent.click(paymentButton);

    await waitFor(() => {
      expect(mockToast.toast).toHaveBeenCalledWith({
        title: 'Zahlungsfehler',
        description: 'Die Zahlung konnte nicht initialisiert werden. Bitte versuche es erneut.',
        variant: 'destructive'
      });
    });
  });

  it('tracks payment events with analytics', async () => {
    const mockProducts = [
      {
        id: 'student_basic',
        name: 'Student Magic Tool Basic',
        price: 97,
        currency: 'eur',
        features: [],
        bonusItems: []
      }
    ];

    const mockPaymentMethods = [
      {
        id: 'card',
        name: 'Kreditkarte',
        description: 'Visa, Mastercard, American Express',
        icon: '💳',
        enabled: true
      }
    ];

    const mockPaymentIntent = {
      id: 'pi_test123',
      clientSecret: 'pi_test123_secret_abc',
      status: 'requires_payment_method'
    };

    (fetch as any)
      .mockResolvedValueOnce({
        json: async () => ({ success: true, products: mockProducts })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentMethods: mockPaymentMethods })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentIntent: mockPaymentIntent })
      });

    render(<PaymentForm {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('Student Magic Tool Basic')).toBeInTheDocument();
    });

    const paymentButton = screen.getByText('🚀 Jetzt kaufen & sofort starten!');
    fireEvent.click(paymentButton);

    await waitFor(() => {
      expect(mockAnalytics.trackEvent).toHaveBeenCalledWith('payment_intent_created', {
        productId: 'student_basic',
        amount: 97,
        personaType: 'student'
      });
    });
  });

  it('formats prices correctly in German locale', async () => {
    const mockProducts = [
      {
        id: 'student_basic',
        name: 'Student Magic Tool Basic',
        price: 97,
        currency: 'eur',
        features: [],
        bonusItems: []
      }
    ];

    const mockPaymentMethods = [
      {
        id: 'card',
        name: 'Kreditkarte',
        description: 'Visa, Mastercard, American Express',
        icon: '💳',
        enabled: true
      }
    ];

    (fetch as any)
      .mockResolvedValueOnce({
        json: async () => ({ success: true, products: mockProducts })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentMethods: mockPaymentMethods })
      });

    render(<PaymentForm {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('97,00 €')).toBeInTheDocument();
    });
  });

  it('shows card form when card payment method is selected', async () => {
    const mockProducts = [
      {
        id: 'student_basic',
        name: 'Student Magic Tool Basic',
        price: 97,
        currency: 'eur',
        features: [],
        bonusItems: []
      }
    ];

    const mockPaymentMethods = [
      {
        id: 'card',
        name: 'Kreditkarte',
        description: 'Visa, Mastercard, American Express',
        icon: '💳',
        enabled: true
      }
    ];

    (fetch as any)
      .mockResolvedValueOnce({
        json: async () => ({ success: true, products: mockProducts })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentMethods: mockPaymentMethods })
      });

    render(<PaymentForm {...defaultProps} />);

    await waitFor(() => {
      expect(screen.getByText('💳 Kreditkarten-Daten')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('Max Mustermann')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('1234 5678 9012 3456')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('MM/YY')).toBeInTheDocument();
      expect(screen.getByPlaceholderText('123')).toBeInTheDocument();
    });
  });

  it('disables payment button when no product is selected', async () => {
    const mockPaymentMethods = [
      {
        id: 'card',
        name: 'Kreditkarte',
        description: 'Visa, Mastercard, American Express',
        icon: '💳',
        enabled: true
      }
    ];

    (fetch as any)
      .mockResolvedValueOnce({
        json: async () => ({ success: true, products: [] })
      })
      .mockResolvedValueOnce({
        json: async () => ({ success: true, paymentMethods: mockPaymentMethods })
      });

    render(<PaymentForm {...defaultProps} />);

    await waitFor(() => {
      const paymentButton = screen.getByText('🚀 Jetzt kaufen & sofort starten!');
      expect(paymentButton).toBeDisabled();
    });
  });
}); 