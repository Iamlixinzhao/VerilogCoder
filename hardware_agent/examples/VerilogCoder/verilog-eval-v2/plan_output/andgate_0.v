module TopModule
(
  input  logic a,
  input  logic b,
  output logic out
);

  // Implement the 2-input AND gate logic
  always @(*) begin
    out = a & b;
  end

endmodule