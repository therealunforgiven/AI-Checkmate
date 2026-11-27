Search Topic: Micsig oscilloscope BMW N52 BSD alternator water pump oil sensor fault isolation

### Topic: Micsig oscilloscope BMW N52 BSD alternator water pump oil sensor fault isolation

#### Synthesized Markdown Notes:

**Source 1: BMW BSD Bus Diagnosis: Fix Alternator, IBS, & Water Pump ...BSD and waterpump - BimmerprofsWeird BSD communication error - BimmerFest BMW ForumN52 BSD codes and voltage issues - e90post.comHow to troubleshoot the BSD bus (IBS, Alternator, Water...BMW Oil Sensor Malfunction Symptoms: Fix N52 N54 B58 Level ...BSD Protocol input - MaxxECU (https://www.youtube.com/watch?v=5A1uvQULf0Q)**

In this video, we dive into the BMW BSD bus communication network to track down what's causing a check engine light. I walk you through my exact isolation diagnostic strategy to find the...

- The DME fault memory contained every possible fault related to the BSD data network.
- Components connected to BSD: IBS, oil quality/level/temperature sensor, alternator, and water pump.
- Fault in BSD line can cause electrical supply problems.
- Fault isolation: unplug components on the BSD line one at a time to see how it reacts.

**Source 2: BSD and waterpump - Bimmerprofs (https://bimmerprofs.com/bsd-and-waterpump/)**

This entry covers a case with a rare defect. It is also worth describing the symptoms that typically point to BSD problems on modern petrol engines.

- The patient was an E9X with an N55 petrol engine.
- The car had power supply problems despite a new AGM battery.
- The water pump started running as soon as the car was unlocked and kept running even after it was locked.
- The DME fault memory contained every possible fault related to the BSD data network.
- Components connected to BSD: IBS, oil quality/level/temperature sensor, alternator, and water pump.
- If the water pump receives no command over BSD, it runs in emergency mode to prevent engine overheating.
- LIN driver can block the network if damaged.
- LIN signal on the oscillogram reaches a maximum of about 0.5 to 0.8 V if only the transistor is damaged.
- If the diode in series with the transistor is also damaged, no LIN signal is visible at all.
- The water pump was replaced.

**Source 3: Weird BSD communication error - BimmerFest BMW Forum (https://www.bimmerfest.com/threads/weird-bsd-communication-error.1470032/)**

The fault lies in one of the components on the BSD line. With a faulty BSD line, the alternator will still charge as required, but there will be no "controlled disconnection" by the DME for current management.
