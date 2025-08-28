module TopModule
(
  input  logic [31:0] in,
  output logic [31:0] out
);

  // Declare a wire to hold the reversed byte order
  logic [31:0] reversed_in;

  // Reverse byte order logic
  always @(*) begin
    reversed_in[31:24] = in[7:0];
    reversed_in[23:16] = in[15:8];
    reversed_in[15:8]  = in[23:16];
    reversed_in[7:0]   = in[31:24];
  end

  // Assign the reversed byte order to the output
  assign out = reversed_in;

endmodule