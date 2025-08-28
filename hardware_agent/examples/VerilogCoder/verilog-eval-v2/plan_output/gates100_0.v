module TopModule
(
  input  logic [99:0] in,
  output logic        out_and,
  output logic        out_or,
  output logic        out_xor
);

  // Combinational logic for 100-input gates

  always @(*) begin
    out_and = &in; // AND reduction operator
    out_or  = |in; // OR reduction operator
    out_xor = ^in; // XOR reduction operator
  end

endmodule