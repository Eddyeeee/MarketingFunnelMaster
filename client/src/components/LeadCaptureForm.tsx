import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useMutation } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { toast } from "@/hooks/use-toast";

const leadSchema = z.object({
  email: z.string().email("Bitte gib eine gültige E-Mail-Adresse ein"),
  firstName: z.string().min(2, "Bitte gib deinen Vornamen ein"),
  lastName: z.string().optional(),
  phone: z.string().optional(),
});

type LeadFormData = z.infer<typeof leadSchema>;

interface LeadCaptureFormProps {
  funnel: string;
  source: string;
  onSubmit?: (data: LeadFormData) => void;
  buttonText?: string;
  showPhone?: boolean;
  showLastName?: boolean;
}

export default function LeadCaptureForm({ 
  funnel, 
  source, 
  onSubmit,
  buttonText = "Kostenlosen Zugang sichern",
  showPhone = false,
  showLastName = false
}: LeadCaptureFormProps) {
  const form = useForm<LeadFormData>({
    resolver: zodResolver(leadSchema),
    defaultValues: {
      email: "",
      firstName: "",
      lastName: "",
      phone: ""
    }
  });

  const leadMutation = useMutation({
    mutationFn: async (data: LeadFormData) => {
      const leadData = {
        ...data,
        funnel,
        source
      };
      const response = await apiRequest('POST', '/api/leads', leadData);
      return response.json();
    },
    onSuccess: (data) => {
      toast({
        title: "Erfolgreich!",
        description: "Deine Daten wurden gespeichert. Du erhältst gleich eine E-Mail von uns.",
      });
      onSubmit?.(form.getValues());
      form.reset();
    },
    onError: (error) => {
      toast({
        title: "Fehler",
        description: "Beim Speichern deiner Daten ist ein Fehler aufgetreten. Bitte versuche es erneut.",
        variant: "destructive"
      });
    }
  });

  const handleSubmit = (data: LeadFormData) => {
    leadMutation.mutate(data);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
        <div className={`grid gap-4 ${showLastName ? 'md:grid-cols-2' : 'grid-cols-1'}`}>
          <FormField
            control={form.control}
            name="firstName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Vorname *</FormLabel>
                <FormControl>
                  <Input placeholder="Dein Vorname" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          
          {showLastName && (
            <FormField
              control={form.control}
              name="lastName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nachname</FormLabel>
                  <FormControl>
                    <Input placeholder="Dein Nachname" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          )}
        </div>
        
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>E-Mail-Adresse *</FormLabel>
              <FormControl>
                <Input type="email" placeholder="deine@email.de" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        
        {showPhone && (
          <FormField
            control={form.control}
            name="phone"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Telefonnummer (optional)</FormLabel>
                <FormControl>
                  <Input type="tel" placeholder="Deine Telefonnummer" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        )}
        
        <Button 
          type="submit" 
          className="w-full gradient-cta hover:bg-q-accent-dark text-white py-3 text-lg font-semibold"
          disabled={leadMutation.isPending}
        >
          {leadMutation.isPending ? 'Wird verarbeitet...' : buttonText}
        </Button>
        
        <p className="text-xs text-q-neutral-medium text-center">
          Mit dem Absenden stimmst du unseren Datenschutzbestimmungen zu. 
          Du kannst dich jederzeit wieder abmelden.
        </p>
      </form>
    </Form>
  );
}
