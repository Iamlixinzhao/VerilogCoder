module TopModule
(
  input  logic clk,
  input  logic areset,
  input  logic train_valid,
  input  logic train_taken,
  output logic [1:0] state
);

  // State register
  logic [1:0] state_next;
  logic [1:0] state_reg;

  always @(posedge clk or posedge areset) begin
    if (areset) begin
      state_reg <= 2'b01; // Reset to weakly not-taken
    end else begin
      state_reg <= state_next;
    end
  end

  // Next state combinational logic
  always @(*) begin
    state_next = state_reg;
    if (train_valid) begin
      if (train_taken) begin
        if (state_reg < 2'b11) begin
          state_next = state_reg + 1;
        end
      end else begin
        if (state_reg > 2'b00) begin
          state_next = state_reg - 1;
        end
      end
    end
    // No need to handle train_valid = 0 case explicitly as state_next = state_reg by default
  end

  // Assign the current counter value to the output port state
  assign state = state_reg;

endmodule