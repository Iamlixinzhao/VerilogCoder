module TopModule
(
  input  logic clk,
  input  logic reset,
  output logic [3:0] q
);

  // Counter register
  logic [3:0] count;

  always @(posedge clk) begin
    if (reset) begin
      count <= 4'b0001; // Reset counter to 1
    end else if (count == 4'b1010) begin
      count <= 4'b0001; // Reset counter to 1 after reaching 10
    end else begin
      count <= count + 1; // Increment counter
    end
  end

  // Assign the counter value to the output
  assign q = count;

endmodule