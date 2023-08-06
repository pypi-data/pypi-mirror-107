program test_abmethod_squarewave
  use ABMethod, only: dagrt_state_type, &
    timestep_initialize => initialize, &
    timestep_run => run, &
    timestep_shutdown => shutdown

  implicit none

  type(dagrt_state_type), target :: state
  type(dagrt_state_type), pointer :: state_ptr

  real*8, dimension(2) :: initial_condition, true_sol
  integer, dimension(2) :: ntrips

  integer run_count
  real*8 t_fin
  parameter (run_count=2, t_fin=1d0)

  real*8, dimension(run_count):: dt_values, errors

  real*8 est_order, min_order

  integer stderr
  parameter(stderr=0)

  integer istep, irun, k

  ! start code ----------------------------------------------------------------

  state_ptr => state

  initial_condition(1) = 2
  initial_condition(2) = 2.3

  ntrips(1) = 20
  ntrips(2) = 50

  k = 0

  do irun = 1,run_count
    dt_values(irun) = t_fin/ntrips(irun)

    call timestep_initialize( &
      dagrt_state=state_ptr, &
      state_y=initial_condition, &
      dagrt_t=0d0, &
      dagrt_dt=dt_values(irun))

    do istep = 1,ntrips(irun)
      if (k == 1) then
        state%dagrt_dt = dt_values(irun)/4
        k = 0
      else
        state%dagrt_dt = dt_values(irun)
        k = 1
      endif
      call timestep_run(dagrt_state=state_ptr)
    enddo

    true_sol = initial_condition * exp(-2*state%ret_time_y)
    errors(irun) = sqrt(sum((true_sol-state%ret_state_y)**2))

    call timestep_shutdown(dagrt_state=state_ptr)
    write(*,*) 'done'
  enddo

  min_order = MIN_ORDER
  est_order = log(errors(2)/errors(1))/log(dt_values(2)/dt_values(1))

  write(*,*) 'estimated order:', est_order
  if (est_order < min_order) then
    write(stderr,*) 'ERROR: achieved order too low:', est_order, ' < ', &
        min_order
  endif

end program
