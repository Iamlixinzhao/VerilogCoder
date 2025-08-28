module TopModule
(
  input  logic clk,
  input  logic a,
  output logic q
);

  // Internal register to hold the state of q
  logic q_reg;

  always @(posedge clk) begin
    if (a) begin
      q_reg <= 0;
    end else begin
      q_reg <= 1;
    end
  end

  // Assign the internal register to the output
  assign q = q_reg;

endmodule