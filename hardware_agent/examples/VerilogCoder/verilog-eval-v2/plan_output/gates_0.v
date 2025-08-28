module TopModule
(
  input  logic a,
  input  logic b,
  output logic out_and,
  output logic out_or,
  output logic out_xor,
  output logic out_nand,
  output logic out_nor,
  output logic out_xnor,
  output logic out_anotb
);

  // Combinational logic for each output

  assign out_and  = a & b; // Implementing the logic for out_and as the AND operation between inputs a and b
  assign out_or   = a | b; // Implementing the logic for out_or as the OR operation between inputs a and b
  assign out_xor  = a ^ b; // Implementing the logic for out_xor as the XOR operation between inputs a and b
  assign out_nand = ~(a & b); // Implementing the logic for out_nand as the NAND operation between inputs a and b
  assign out_nor  = ~(a | b); // Implementing the logic for out_nor as the NOR operation between inputs a and b
  assign out_xnor = a ~^ b; // Implementing the logic for out_xnor as the XNOR operation between inputs a and b
  assign out_anotb = a & ~b; // Implementing the logic for out_anotb as the AND-NOT operation between input a and the negation of input b

endmodule