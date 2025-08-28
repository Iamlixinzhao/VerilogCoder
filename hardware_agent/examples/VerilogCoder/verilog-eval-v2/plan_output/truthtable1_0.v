module TopModule
(
  input  logic x3,
  input  logic x2,
  input  logic x1,
  output logic f
);

  // Combinational logic for the truth table
  always @(*) begin
    f = (x2 & ~x3) | (x1 & x3) | (x1 & x2);
  end

endmodule