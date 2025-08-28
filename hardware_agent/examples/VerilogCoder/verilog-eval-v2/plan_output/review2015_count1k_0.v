module TopModule
(
  input  logic clk,
  input  logic reset,
  output logic [9:0] q
);

  // Counter register
  logic [9:0] count;

  always @(posedge clk) begin
    if (reset) begin
      count <= 10'b0;
    end else begin
      if (count == 10'd999) begin
        count <= 10'b0;
      end else begin
        count <= count + 1;
      end
    end
  end

  // Output assignment
  assign q = count;

endmodule