module TopModule
(
  input  logic [5:0] y,
  input  logic       w,
  output logic       Y1,
  output logic       Y3
);

  // Combinational logic for Y1 and Y3

  always @(*) begin
    // Y1 is the input of state flip-flop y[1] (state B)
    Y1 = (y[0] & w);

    // Y3 is the input of state flip-flop y[3] (state D)
    Y3 = (y[1] & ~w) | (y[2] & ~w) | (y[4] & ~w) | (y[5] & ~w);
  end

endmodule