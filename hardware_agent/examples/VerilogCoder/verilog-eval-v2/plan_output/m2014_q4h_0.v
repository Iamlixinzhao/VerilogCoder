module TopModule
(
  input  logic in,
  output logic out
);

  // Initialize output
  initial begin
    out = 0;
  end

  // Combinational logic
  always @(*) begin
    out = in;
  end

endmodule