module TopModule
(
  input  logic       clk,
  input  logic       areset,
  input  logic [7:0] d,
  output logic [7:0] q
);

  // Sequential logic for 8 D flip-flops with asynchronous reset
  always @(posedge clk or posedge areset) begin
    if (areset) begin
      q <= 8'b0;
    end else begin
      q <= d;
    end
  end

endmodule