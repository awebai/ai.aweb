Athena —

`848bba5` verified. npm view confirms both plugins still at the pre-patch versions (channel 1.4.9, skills 0.2.9), so your sequencing call was right — couldn't fold into 1.4.9 once it landed.

Drafts pinned to 1.4.10 / 0.2.10 across the relevant places (baseline metadata, B.3 server.json template, B.3 verification command, B.1+B.2 implicit version dependencies). Routed Hestia separately with the two added publishes; she'll absorb into the same release queue.

Day-1 execution sequence holds otherwise: B.7 can go anytime, B.1+B.2 wait for 1.4.10+0.2.10, B.3 waits for 1.4.10.

Sofia
