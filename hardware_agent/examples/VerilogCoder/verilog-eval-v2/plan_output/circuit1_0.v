module TopModule
(
  input  logic a,
  input  logic b,
  output logic q
);

  // Combinational logic
  always @(*) begin
    q = a & b;
  end

endmodule