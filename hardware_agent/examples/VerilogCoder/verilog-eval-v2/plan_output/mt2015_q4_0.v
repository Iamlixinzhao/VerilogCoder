module ModuleA
(
  input  logic x,
  input  logic y,
  output logic z
);
  // Implementing the boolean function z = (x^y) & x
  assign z = (x ^ y) & x;
endmodule

module ModuleB
(
  input  logic x,
  input  logic y,
  output logic z
);
  // Implementing the behavior based on the simulation waveform
  always @(*) begin
    if (x == 0 && y == 0) begin
      z = 1;
    end else if (x == 1 && y == 0) begin
      z = 0;
    end else if (x == 0 && y == 1) begin
      z = 0;
    end else if (x == 1 && y == 1) begin
      z = 1;
    end
  end
endmodule

module TopModule
(
  input  logic x,
  input  logic y,
  output logic z
);

  // Intermediate signals for submodule outputs
  logic a1_out, a2_out, b1_out, b2_out;
  logic or_out, and_out;

  // Submodule A instances
  ModuleA a1 (
    .x(x),
    .y(y),
    .z(a1_out)
  );

  ModuleA a2 (
    .x(x),
    .y(y),
    .z(a2_out)
  );

  // Submodule B instances
  ModuleB b1 (
    .x(x),
    .y(y),
    .z(b1_out)
  );

  ModuleB b2 (
    .x(x),
    .y(y),
    .z(b2_out)
  );

  // OR gate for first pair of A and B submodules
  assign or_out = a1_out | b1_out;

  // AND gate for second pair of A and B submodules
  assign and_out = a2_out & b2_out;

  // XOR gate for final output
  assign z = or_out ^ and_out;

endmodule