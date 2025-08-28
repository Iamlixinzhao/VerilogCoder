module TopModule
(
  input  logic [3:0] x,
  output logic       f
);

  // Combinational logic to implement the function based on the Karnaugh map

  always @(*) begin
    case (x)
      4'b0000, 4'b0001: f = 1'b1; // For (x[3], x[2]) = (0,0) and x[1:0] = 00, 01
      4'b0100, 4'b0101, 4'b0110: f = 1'b1; // For (x[3], x[2]) = (0,1) and x[1:0] = 00, 01, 10
      4'b1100, 4'b1110, 4'b1111: f = 1'b1; // For (x[3], x[2]) = (1,1) and x[1:0] = 00, 11, 10
      // For (x[3], x[2]) = (1,0), all outputs are 0
      4'b1000, 4'b1001, 4'b1010, 4'b1011: f = 1'b0;
      default: f = 1'b0;
    endcase
  end

endmodule