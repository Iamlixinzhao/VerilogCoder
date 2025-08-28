module TopModule
(
  input  logic clock,
  input  logic a,
  output logic p,
  output logic q
);

  // Latch for p
  always @(*) begin
    if (clock) begin
      p = a;
    end
  end

  // Flip-flop for q
  always @(negedge clock) begin
    q <= p;
  end

endmodule