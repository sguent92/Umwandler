!	
!  Simpack Input Function File	
!	
header.begin	
  file.type    = 'afs'      ! SIMPACK File Type: Input Function	
  file.version = 1.0        ! Release	
header.end	
	
arrfunc.begin	
  type          	 ='z(xi,yj)'                        ! Input Function Type
  name(1)       = 'Radial Force'                    ! Input Function Name z1	
  name(2)       = 'Tangetial Force'                 ! Input Function Name z2 	
 name(3)       = 'Reaction Torque'                 ! Input Function Name z3	
  eval.type     = 'linear-linear'                   ! Interpolation	
  x.unit        = 'rad'                             ! Unit x: 	
  y.unit        = 'rad'                             ! Unit y: 	
  z.unit(1)     = 'N'                               ! Unit z1: force [N]	
  z.unit(2)     = 'N'                               ! Unit z2: force [N]	
z.unit(3)     = 'Nm'                              ! Unit z2: torque [Nm]	
  data.begin	
   x.begin	
   !  xi	
   !  rotor_angle	
