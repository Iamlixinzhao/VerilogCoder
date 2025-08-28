module TopModule
(
  input  logic       clk,
  input  logic [7:0] d,
  output logic [7:0] q
);

  // Sequential logic for 8 D flip-flops
  always @(posedge clk) begin
    q <= d;
  end

  // Initialize q to 0
  initial begin
    q = 8'b00000000;
  end

endmodule