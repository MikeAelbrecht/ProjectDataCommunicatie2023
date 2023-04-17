#define I2C_SLAVE_ADDRESS 0x13 // the 7-bit address (remember to change this when adapting this example)
// Get this from https://github.com/rambo/TinyWire
#include <TinyWireS.h>
// The default buffer size, Can't recall the scope of defines right now
#ifndef TWI_RX_BUFFER_SIZE
#define TWI_RX_BUFFER_SIZE ( 16 )
#endif

#define R_pin 1
#define G_pin 3
#define B_pin 4

bool handleData = false;
uint8_t dataArray[2];

volatile uint8_t i2c_regs[] =
{
  0xDE, 
  0xAD, 
  0xBE, 
  0xEF, 
};

// Tracks the current register pointer position
volatile byte reg_position;
const byte reg_size = sizeof(i2c_regs);

/**
 * This is called for each read request we receive, never put more than one byte of data (with TinyWireS.send) to the 
 * send-buffer when using this callback
 */
void requestEvent()
{  
  TinyWireS.send(i2c_regs[reg_position]);
  // Increment the reg position on each read, and loop back to zero
  reg_position++;
  if (reg_position >= reg_size)
  {
    reg_position = 0;
  }
}

/**
 * The I2C data received -handler
 *
 * This needs to complete before the next incoming transaction (start, data, restart/stop) on the bus does
 * so be quick, set flags for long running tasks to be called from the mainloop instead of running them directly,
 */
void receiveEvent(uint8_t byte_count)
{
  if (!TinyWireS.available() || byte_count != 2)
  {
    for (int i = 0; i < 2; i++)
    {
      digitalWrite(R_pin, HIGH);
      tws_delay(100);
      digitalWrite(R_pin, LOW); 
      tws_delay(100);
    }
    
    return;
  } 

  handleData = true;

  dataArray[0] = TinyWireS.receive();
  dataArray[1] = TinyWireS.receive();

  if (dataArray[0] == 'r' && dataArray[1] == 'a') 
  {
    digitalWrite(R_pin, HIGH);
    digitalWrite(G_pin, LOW);
    digitalWrite(B_pin, LOW);  
  }

  if (dataArray[0] == 'g' && dataArray[1] == 'a')
  {
    digitalWrite(G_pin, HIGH);
    digitalWrite(R_pin, LOW);
    digitalWrite(B_pin, LOW); 
  }

  if (dataArray[0] == 'b' && dataArray[1] == 'a') 
  {
    digitalWrite(B_pin, HIGH);
    digitalWrite(R_pin, LOW);
    digitalWrite(G_pin, LOW);
  }

  if (dataArray[0] == 'a' && dataArray[1] == 'u')
  {
    digitalWrite(R_pin, LOW);
    digitalWrite(G_pin, LOW);
    digitalWrite(B_pin, LOW);  
  }

  uint8_t data =  dataArray[1];
  TinyWireS.send(data);
}

void setup()
{
  TinyWireS.begin(I2C_SLAVE_ADDRESS);
  TinyWireS.onReceive(receiveEvent);
  TinyWireS.onRequest(requestEvent);
  
  // Whatever other setup routines ?
  pinMode(R_pin, OUTPUT);
  pinMode(G_pin, OUTPUT);
  pinMode(B_pin, OUTPUT);

  digitalWrite(B_pin, HIGH);
  delay(500);
  digitalWrite(B_pin, LOW);
}

void loop()
{
  TinyWireS_stop_check();
}
