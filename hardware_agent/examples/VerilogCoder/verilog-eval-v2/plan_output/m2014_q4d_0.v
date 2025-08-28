module TopModule
(
  input  logic clk,
  input  logic in,
  output logic out
);

  // Intermediate signal for XOR output
  logic xor_out;

  // Initialize out to 0
  initial begin
    out = 0;
  end

  // XOR gate implementation
  always @(*) begin
    xor_out = in ^ out;
  end

  // D flip-flop implementation
  always @(posedge clk) begin
    out <= xor_out;
  end

endmodule