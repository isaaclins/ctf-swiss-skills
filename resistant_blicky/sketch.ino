#define GET_BIT(array, bitpos) (((array[(bitpos) / 8] >> (7 - ((bitpos) % 8))) & 1))
#define LEN 64

const uint8_t data[] = { 0xE4, 0x7F, 0x23, 0x9C, 0x7C, 0xE2, 0x47, 0x30 };

int main(void) {
  DDRB = 0x20;

  TCCR1A = 0x00;
  TCCR1B = 0x01;
  TIMSK1 = 0x01;

  sei();

  while(1) {
    ADMUX = 0x40;
    ADCSRA = 0xC0;
    while (ADCSRA & 0x40);
    uint16_t r = (ADCH << 8) | ADCL;
    TCCR1B = map(r, 0, 0x03FF, 1, 5);
    delay(100);
  }
}

ISR(TIMER1_OVF_vect) {
  static uint8_t i = 0;
  PORTB ^= GET_BIT(data, i) << 5;
  ++i %= LEN;
}

// i think the simulator has a bug:
// the voltage divider doesn't work as expected
// maybe replace with a potentiometer?
