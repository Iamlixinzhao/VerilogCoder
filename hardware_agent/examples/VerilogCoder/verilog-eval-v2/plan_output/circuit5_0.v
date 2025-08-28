module TopModule
(
  input  logic [3:0] a,
  input  logic [3:0] b,
  input  logic [3:0] c,
  input  logic [3:0] d,
  input  logic [3:0] e,
  output logic [3:0] q
);

  always @(*) begin
    case (c)
      4'b0000: q = b; // When c is 0
      4'b0001: q = e; // When c is 1
      4'b0010: q = a; // When c is 2
      4'b0011: q = d; // When c is 3
      default: q = 4'b1111; // When c is 4 to f
    endcase
  end

endmodule