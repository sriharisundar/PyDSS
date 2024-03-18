from typing import Union, Annotated

from pydantic import BaseModel, Field, model_validator

from PyDSS.pyControllers.enumerations import CategoryI, CategoryII, CategoryIII, PvStandard, VoltageCalcModes, RideThroughCategory, PermissiveOperation, MayTripOperation, MultipleDisturbances



class BaseControllerModel(BaseModel):
    ...
    
    
class PvVoltageRideThruModel(BaseControllerModel):
    """Data model for the PV voltage ride through controller"""
    
    kva : Annotated[
        float,
        Field(4.0, ge=0.0, description="kVA capacity of the inverter (AC-side)."),
    ] 
    max_kw: Annotated[
        float,
        Field(4.0, ge=0.0, description="kW capacity of the PV system (DC-side)."),
    ] 
    voltage_calc_mode: Annotated[
        VoltageCalcModes,
        Field(VoltageCalcModes.MAX, description="Voltage values used to calculate Var support from the inverter (Maximum or Average)."),
    ] 
    follow_standard: Annotated[
        PvStandard,
        Field(PvStandard.IEEE_1547_2018, description="IEEE standard the inverter is following."),
    ] 
    ride_through_category : Annotated[
        RideThroughCategory,
        Field(RideThroughCategory.CATEGORY_I, description="PV ride-through category fot the inverter (see IEEE 1547-2018 std for more information)."),
    ] 
    ov_2_pu: Annotated[
        float,
        Field(CategoryI.OV2_PU.value, description="Upper bound for the over-voltage region."),
    ] 
    ov_2_ct_sec: Annotated[
        float,
        Field(CategoryI.OV2_CT_SEC.value, description="Trip duration setting if the upper bound of the over-voltage region is violated."),
    ] 
    ov_1_pu: Annotated[
        float,
        Field(CategoryI.OV1_PU.value, description="Lower bound for the over-voltage region."),
    ] 
    ov_1_ct_sec: Annotated[
        float,
        Field(CategoryI.OV1_CT_SEC.value, description="Trip duration setting if the lower bound of the over-voltage region is violated."),
    ] 
    uv_1_pu: Annotated[
        float,
        Field(CategoryI.UV1_PU.value, description="Upper bound for the under-voltage region."),
    ] 
    uv_1_ct_sec: Annotated[
        float,
        Field(CategoryI.UV1_CT_SEC.value, description="Trip duration setting if the upper bound of the under-voltage region is violated."),
    ] 
    uv_2_pu:  Annotated[
        float,
        Field(CategoryI.UV2_PU.value, description="Lower bound for the under-voltage region."),
    ]   
    uv_2_ct_sec: Annotated[
        float,
        Field(CategoryI.UV2_CT_SEC.value, description="Trip duration setting if the upper bound of the under-voltage region is violated."),
    ] 
    reconnect_deadtime_sec : Annotated[
        float,
        Field(3000.0, ge=0.0, description=""),
    ] 
    reconnect_pmax_time_sec : Annotated[
        float,
        Field(300.0, ge=0.0, description="Reconnect after a trip event. PV system will connect back once this time has elapsed and the system voltage is within bounds."),
    ] 
    permissive_operation: Annotated[
        PermissiveOperation,
        Field(PermissiveOperation.CURRENT_LIMITED, description="Defines behavior of the system within the 'permissive operation' region. (see IEEE 1547-2018 std for more information)."),
    ] 
    may_trip_operation: Annotated[
        MayTripOperation,
        Field(MayTripOperation.TRIP, description="Defines behavior of the system within the 'may trip' region. (see IEEE 1547-2018 std for more information)."),
    ] 
    multiple_disturdances: Annotated[
        MultipleDisturbances,
        Field(MultipleDisturbances.TRIP, description="Defines behavior of the system after multiple disturbances. (see IEEE 1547-2018 std for more information)."),
    ] 

    @model_validator(mode='after')
    def update_settings(self) -> 'PvVoltageRideThruModel':
        cat1 = self.ride_through_category == RideThroughCategory.CATEGORY_I
        cat2 = self.ride_through_category == RideThroughCategory.CATEGORY_II
          
        self.ov_2_pu = CategoryI.OV2_PU.value if cat1 else CategoryII.OV2_PU.value if cat2 else CategoryIII.OV2_PU.value
        self.ov_1_pu = CategoryI.OV1_PU.value if cat1 else CategoryII.OV1_PU.value if cat2 else CategoryIII.OV1_PU.value
        self.uv_2_pu = CategoryI.UV2_PU.value if cat1 else CategoryII.UV2_PU.value if cat2 else CategoryIII.UV2_PU.value
        self.uv_1_pu = CategoryI.UV1_PU.value if cat1 else CategoryII.UV1_PU.value if cat2 else CategoryIII.UV1_PU.value     
        self.ov_2_ct_sec = CategoryI.OV2_CT_SEC.value if cat1 else CategoryII.OV2_CT_SEC.value if cat2 else CategoryIII.OV2_CT_SEC.value
        self.ov_1_ct_sec = CategoryI.OV1_CT_SEC.value if cat1 else CategoryII.OV1_CT_SEC.value if cat2 else CategoryIII.OV1_CT_SEC.value
        self.uv_2_ct_sec = CategoryI.UV2_CT_SEC.value if cat1 else CategoryII.UV2_CT_SEC.value if cat2 else CategoryIII.UV2_CT_SEC.value
        self.uv_1_ct_sec = CategoryI.UV1_CT_SEC.value if cat1 else CategoryII.UV1_CT_SEC.value if cat2 else CategoryIII.UV1_CT_SEC.value
        
        return self



class PvSmartController(BaseControllerModel):
    kvar_limit: Annotated[
        float,
        Field(1.76, ge=0.0, description="kVar capacity of the PV system."),
    ] 
    pct_p_cutin: Annotated[
        float,
        Field(10.0, ge=0.0, le=100.0, description="Percentage of kVA rating of inverter. When the inverter is OFF, the power from the system must be greater than this for the inverter to turn on"),
    ] 
    pct_p_cutout: Annotated[
        float,
        Field(10.0, ge=0.0, le=100.0, description="Percentage of kVA rating of inverter. When the inverter is ON, the inverter turns OFF when the power from the array drops below this value."),
    ] 
    enable_pf_limit: Annotated[
        bool,
        Field(False, description="Enable flag to apply power factor limits on the inverter output"),
    ] 
    pf_min: Annotated[
        float,
        Field(0.95, ge=0.0, le=1.0, description="Minimum allowable powerfactor for the system. 'enable_pf_limit' should be enable for the constraint to be implemented."),
    ] 
    
class MotorStallSimpleSettings(BaseModel):
    p_fault: Annotated[
        float,
        Field(3.5, ge=3.0, le=5.0, description="Active power multiplier post fault."),
    ] 
    q_fault: Annotated[
        float,
        Field(5.0, ge=3.0, le=7.0, description="Reactive power multiplier post fault."),
    ] 
    v_stall: Annotated[
        float,
        Field(0.55, ge=0.53, le=0.58, description="Per unit voltage below which the motor will stall."),
    ] 
    t_protection: Annotated[
        float,
        Field(0.95, ge=0.0, le=15.0, description="Time [sec] after stall the motor will disconnect."),
    ] 
    t_reconnect: Annotated[
        float,
        Field(6.0, ge=5.0, le=7.0, description="Time duration [sec] after which the motor will reconnect."),
    ] 
    

class MotorStallSettings(BaseModel):
    k_p1:  Annotated[
        float,
        Field(0 , description="Real power constant for running state 111"),
    ] 
    n_p1:  Annotated[
        float,
        Field(1.0, description="Real power exponent for running state 1"),
    ] 
    k_p2:  Annotated[
        float,
        Field(12.0, description="Real power constant for running state 2"),
    ] 
    n_p2:  Annotated[
        float,
        Field(3.2, description="Real power exponent for running state 2"),
    ] 
    k_q1:  Annotated[
        float,
        Field(6.0, description="Reactive power constant for running state 1"),
    ] 
    n_q1:  Annotated[
        float,
        Field(2.0, description="Reactive power exponent for running state 1"),
    ] 
    k_q2:  Annotated[
        float,
        Field(11.0, description="Reactive power constant for running state 2"),
    ] 
    n_q2:  Annotated[
        float,
        Field(2.5, description="Reactive power exponent for running state 2."),
    ] 
    t_th:  Annotated[
        float,
        Field(4.0, description="Varies based on manufacturer and external factors - sensitivity analysis required"),
    ] 
    f_rst:  Annotated[
        float,
        Field(0.2, description="Captures diversity in load; also based on testing (fraction of motors capable of restart)."),
    ] 
    lf_adj:  Annotated[
        float,
        Field(0.0, description="Load factor adjustment to the stall voltage10"),
    ] 
    t_th1t:  Annotated[
        float,
        Field(0.7, description="Assumed tripping starting at 70% temperature"),
    ] 
    t_th2t:  Annotated[
        float,
        Field(1.9, description="Assumed all tripped at 190% temperature"),
    ] 
    p_fault: Annotated[
        float,
        Field(3.5, ge=3.0, le=5.0, description="Active power multiplier post fault."),
    ] 
    q_fault: Annotated[
        float,
        Field(5.0, ge=3.0, le=7.0, description="Reactive power multiplier post fault."),
    ] 
    v_stall:  Annotated[
        float,
        Field(0.55, ge=0.45, le=0.60,  description="Stall voltage (range) based on laboratory testing"),
    ] 
    v_break:  Annotated[
        float,
        Field(0.86, description="Compressor motor 'breakdown' voltage (pu)"),
    ] 
    v_rstrt: Annotated[
        float,
        Field(0.95, description="Reconnect when acceptable voltage met"),
    ] 
    t_stall:  Annotated[
        float,
        Field(0.032, description="Stall time (range) based on laboratory testing"),
    ] 
    t_restart:  Annotated[
        float,
        Field(0.300, description="Induction motor restart time is relatively short"),
    ] 
    rated_pf:  Annotated[
        float,
        Field(0.939, description="Assumed slightly inductive motors load"),
    ] 
    r_stall_pu:  Annotated[
        float,
        Field(0.100, description="Based on laboratory testing results of residential air-conditioners."),
    ]
    x_stall_pu:  Annotated[
        float,
        Field(0.100, description="Based on laboratory testing results of residential air-conditioners."),
    ]  
    
