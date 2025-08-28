module TopModule
(
  input  logic clk,
  input  logic j,
  input  logic k,
  output logic Q
);

  // Internal signal for storing the state of Q
  logic Qold;

  initial begin
    Qold = 0; // Initialize Qold to a known state
  end

  always @(posedge clk) begin
    if (j == 0 && k == 0) begin
      Q <= Q; // No change
    end else if (j == 0 && k == 1) begin
      Q <= 0; // Reset
    end else if (j == 1 && k == 0) begin
      Q <= 1; // Set
    end else if (j == 1 && k == 1) begin
      Q <= ~Q; // Toggle using current Q
    end
    Qold <= Q; // Update Qold to current Q after operations
  end

endmodule