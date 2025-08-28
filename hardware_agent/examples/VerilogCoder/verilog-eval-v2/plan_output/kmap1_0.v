module TopModule
(
  input  logic a,
  input  logic b,
  input  logic c,
  output logic out
);

  // Combinational logic for Karnaugh map implementation
  always @(*) begin
    if ((b & ~c) | (b & c) | a | (~b & c)) begin
      out = 1;
    end else begin
      out = 0;
    end
  end

endmodule