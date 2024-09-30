
from odoo import api, fields, models
from datetime import date, datetime, time, timedelta
from datetime import timedelta
import pyodbc
from pytz import timezone, UTC
from dateutil import relativedelta

class Attendance(models.Model):

    _inherit = "hr.attendance"
    sql_Server_id_max = fields.Integer(readonly=True)
    sql_Server_check_in_id = fields.Integer(readonly=True)
    upload_time = fields.Date(readonly=True)
    area_name = fields.Char(string='Location Name')
    check_in_time = fields.Datetime(string='Check In', compute='_compute_check_in_view_hours', store=True, readonly=True)
    check_out_time = fields.Datetime(string='Check out', compute='_compute_check_out_view_hours', store=True, readonly=True)
    break1 = fields.Float(string='First Break',  compute='_compute_break1_hours', store=True, readonly=True)
    break2 = fields.Float(string='Second Break', compute='_compute_break2_hours', store=True, readonly=True)
    break3 = fields.Float(string='Third Break', compute='_compute_break3_hours', store=True, readonly=True)
    break_in = fields.Datetime(string="Second Break In")
    break_in_2 = fields.Datetime(string="Second Break In")
    break_in_3 = fields.Datetime(string="Third Break In")
    break_out = fields.Datetime(string="Second Break Out")
    break_out_2 = fields.Datetime(string="Second Break Out")
    break_out_3 = fields.Datetime(string="Third Break Out")
    break_in_1_time = fields.Datetime(string='First Break In', compute='_compute_first_break_in_view_hours', store=True, readonly=False)
    break_in_2_time = fields.Datetime(string='Second Break In', compute='_compute_second_break_in_view_hours', store=True, readonly=False)
    break_in_3_time = fields.Datetime(string='Third Break In', compute='_compute_third_break_in_view_hours', store=True, readonly=False)
    break_out_1_time = fields.Datetime(string='First Break Out', compute='_compute_first_break_out_view_hours', store=True, readonly=False)
    break_out_2_time = fields.Datetime(string='Second Break Out', compute='_compute_second_break_out_view_hours', store=True, readonly=False)
    break_out_3_time = fields.Datetime(string='Third Break Out', compute='_compute_third_break_out_view_hours', store=True, readonly=False)
    break_sum = fields.Float(string='Sum Of breaks', compute='_compute_sum_breaks_hours', store=True, readonly=True)
    official_in = fields.Datetime(string="Official In", store=True, readonly=True)
    official_in_1_time = fields.Datetime(string="Official In", compute='_compute_first_official_in_hours', store=True, readonly=False)
    official_out = fields.Datetime(string="Official Out")
    official_out_1_time = fields.Datetime(string='Official Out', compute='_compute_first_official_out_hours', store=True, readonly=False)
    official_in_2 = fields.Datetime(string="Second Official In")
    official_in_2_time = fields.Datetime(string="Second Official In", compute='_compute_second_official_in_hours', store=True, readonly=False)
    official_in_3 = fields.Datetime(string="Third Official In")
    official_in_3_time = fields.Datetime(string='Third Official In', compute='_compute_second_break_in_view_hours', store=True, readonly=False)
    official_out_2 = fields.Datetime(string="Second Official Out")
    official_out_2_time = fields.Datetime(string='Second Official Out', compute='_compute_third_official_in_hours', store=True, readonly=False)
    official_out_3 = fields.Datetime(string="Third Official Out")
    official_out_3_time = fields.Datetime(string='Third Official Out', compute='_compute_third_official_out_hours', store=True, readonly=False)
    official1 = fields.Float(string='1st offecial', compute='_compute_official_hours', store=True, readonly=True)
    official2 = fields.Float(string='2nd official', compute='_compute_official2_hours', store=True, readonly=True)
    official3 = fields.Float(string='3rd official', compute='_compute_official3_hours', store=True, readonly=True)
    official_sum = fields.Float(string='Sum Of Officials', compute='_compute_sum_officails_hours', store=True,
                                readonly=False)
    late_in = fields.Float(string='Late In', store=True, compute='_compute_late', readonly=False)
    early_out = fields.Float(string='Early Out', store=True,
                           readonly=False)
    is_late_check_in = fields.Boolean(compute='_get_is_late_check',
                                              string="Late Check In",
                                              compute_sudo=True, store=True)
    is_early_check_out = fields.Boolean(compute='_get_is_late_check',
                                              string="Early Check Out",
                                              compute_sudo=True, store=True)
    late_in_hours = fields.Float(string="Late In Hours")
    late_price = fields.Float(string="Late Price")
    is_deduction = fields.Boolean(string="Is Deduction")

    @api.depends('check_in')
    def _compute_check_in_view_hours(self):
        for attendance in self:
            if attendance.check_in:
                attendance.check_in_time = attendance.check_in + relativedelta.relativedelta(hours=-3)

    @api.depends('check_out')
    def _compute_check_out_view_hours(self):
        for attendance in self:
            if attendance.check_out:
                attendance.check_out_time = attendance.check_out + relativedelta.relativedelta(hours=-3)



    @api.depends('official_in', 'official_out')
    def _compute_first_official_in_hours(self):
        for attendance in self:
            if attendance.official_in:
                attendance.official_in_1_time = attendance.official_in + relativedelta.relativedelta(hours=-3)

            else:
                attendance.official_in_1_time = False

    @api.depends('official_in', 'official_out')
    def _compute_first_official_out_hours(self):
        for attendance in self:
            if attendance.official_out:
                attendance.official_out_1_time = attendance.official_out + relativedelta.relativedelta(hours=-3)

            else:
                attendance.official_out_1_time = False

    @api.depends('official_in_1_time', 'official_out_1_time')
    def _compute_official_hours(self):
        for attendance in self:
            if attendance.official_out_1_time:
                delta = attendance.official_out_1_time - attendance.official_in_1_time
                attendance.official1 = delta.total_seconds() / 3600.0
            else:
                attendance.official1 = False

    @api.depends('official_in_2', 'official_out_2')
    def _compute_second_official_in_hours(self):
            for attendance in self:
                if attendance.official_in_2:
                    attendance.official_in_2_time = attendance.official_in_2 + relativedelta.relativedelta(hours=-3)

                else:
                    attendance.official_in_2_time = False

    @api.depends('official_in_2', 'official_out_2')
    def _compute_second_official_out_hours(self):
        for attendance in self:
            if attendance.official_out_2:
                attendance.official_out_2_time = attendance.official_out_2 + relativedelta.relativedelta(hours=-3)

            else:
                attendance.official_out_2_time = False

    @api.depends('official_in_2_time', 'official_out_2_time')
    def _compute_official2_hours(self):
        for attendance in self:
            if attendance.official_out_2_time:
                delta = attendance.official_out_2_time - attendance.official_in_2_time
                attendance.official12 = delta.total_seconds() / 3600.0
            else:
                attendance.official2 = False

    @api.depends('official_in_3', 'official_out_3')
    def _compute_third_official_in_hours(self):
        for attendance in self:
            if attendance.official_in_2:
                attendance.official_in_3_time = attendance.official_in_3 + relativedelta.relativedelta(hours=-3)

            else:
                attendance.official_in_3_time = False

    @api.depends('official_in_3', 'official_out_3')
    def _compute_third_official_out_hours(self):
        for attendance in self:
            if attendance.official_out_2:
                attendance.official_out_3_time = attendance.official_out_3 + relativedelta.relativedelta(hours=-3)

            else:
                attendance.official_out_3_time = False

    @api.depends('official_in_3_time', 'official_out_3_time')
    def _compute_official3_hours(self):
        for attendance in self:
            if attendance.official_out_3_time:
                delta = attendance.official_out_3_time - attendance.official_in_3_time
                attendance.official3 = delta.total_seconds() / 3600.0
            else:
                attendance.official3 = False

    @api.depends('break_in_1_time', 'break_out_1_time')
    def _compute_break1_hours(self):
        for attendance in self:
            if attendance.break_out_1_time:
                delta = attendance.break_out_1_time - attendance.break_in_1_time
                attendance.break1 = delta.total_seconds() / 3600.0
            else:
                attendance.break1 = False

    @api.depends('break_in', 'break_out')
    def _compute_first_break_in_view_hours(self):
        for attendance in self:
            if attendance.break_in:
                attendance.break_in_1_time = attendance.break_in + relativedelta.relativedelta(hours=-3)

            else:
                attendance.break_in_1_time = False

    @api.depends('break_in', 'break_out')
    def _compute_first_break_out_view_hours(self):
        for attendance in self:
            if attendance.break_out:
                attendance.break_out_1_time = attendance.break_out + relativedelta.relativedelta(hours=-3)

            else:
                attendance.break_out_1_time = False


    @api.depends('break_in_2', 'break_out_2')
    def _compute_second_break_in_view_hours(self):
        for attendance in self:
            if attendance.break_in_2:
                attendance.break_in_2_time = attendance.break_in_2 + relativedelta.relativedelta(hours=-3)

            else:
                attendance.break_in_2_time = False

    @api.depends('break_in_2', 'break_out_2')
    def _compute_second_break_out_view_hours(self):
        for attendance in self:
            if attendance.break_out_2:
                attendance.break_out_2_time = attendance.break_out_2 + relativedelta.relativedelta(hours=-3)

            else:
                attendance.break_out_2_time = False

    @api.depends('break_in_2_time', 'break_out_2_time')
    def _compute_break2_hours(self):
        for attendance in self:
            if attendance.break_out_2_time:
                delta = attendance.break_out_2_time - attendance.break_in_2_time
                attendance.break2 = delta.total_seconds() / 3600.0
            else:
                attendance.break2 = False



    @api.depends('break_in_3', 'break_out_3')
    def _compute_third_break_in_view_hours(self):
        for attendance in self:
            if attendance.break_in_3:
                attendance.break_in_3_time = attendance.break_in_3 + relativedelta.relativedelta(hours=-3)

            else:
                attendance.break_in_3_time = False

    @api.depends('break_in_3_time', 'break_out_3_time')
    def _compute_break3_hours(self):
        for attendance in self:
            if attendance.break_out_3_time:
                delta = attendance.break_out_3_time - attendance.break_in_3_time
                attendance.break3 = delta.total_seconds() / 3600.0
            else:
                attendance.break3 = False

    @api.depends('break_in_3', 'break_out_3')
    def _compute_third_break_out_view_hours(self):
        for attendance in self:
            if attendance.break_out_3:
                attendance.break_out_3_time = attendance.break_in_3 + relativedelta.relativedelta(hours=-3)

            else:
                attendance.break_out_3_time = False


    @api.depends('official_in', 'official_out')
    def _compute_sum_officails_hours(self):
       for attendance in self:
             if attendance.official3:
                 attendance.official_sum =   attendance.official1 + attendance.official2 + attendance.official3
             elif attendance.official2:
                 attendance.official_sum = attendance.official1 + attendance.official2
             elif attendance.official1:
                 attendance.official_sum =  attendance.official1


    @api.depends('break1', 'break2', 'break3')
    def _compute_sum_breaks_hours(self):
        for attendance in self:
            if attendance.break3:
                attendance.break_sum = attendance.break1 + attendance.break2 + attendance.break3
            elif attendance.break2:
                attendance.break_sum = attendance.break1 + attendance.break2
            elif attendance.break1:
                attendance.break_sum = attendance.break1

    @api.depends('check_in', 'check_out')
    def _compute_late(self):
        for attendance in self:
          #  t1 = timedelta(hours=8, minutes=15).datetime.strptime(self.d, "%H-%M-%S")
            seconds = 86399
            t2 = timedelta(hours=8, minutes=15)
            t3 = timedelta(hours=13, minutes=7)
            t4 = timedelta(hours=21, minutes=0)
          #  dt = datetime.datetime.strptime(str(t2), "%H:%M:%S")
            strg = attendance.check_in
            s1 = strg.strftime("%m/%d/%Y, %H:%M:%S")
          #  strg1 = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
            date_time_str = '18/09/19 08:15:00'

            strg1 =  datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')


            #r1 = datetime.strptime(strg1, '%Y-%m-%d-%H-%M').strftime("%m/%d/%Y, %H:%M:%S")
          #  strg = attendance.check_in
           # tme = strg.timedelta\
           # dt1 = datetime.strptime(r1, '%H:%M:%S')
            #date_time_str = "2017-07-20-10-30"
            #r9 = datetime.strptime(date_time_str, '%Y-%m-%d-%H-%M').time()


        # print(tme)  # 10:30:00
            enter_delta = timedelta(hours=strg1.hour, minutes=strg1.minute)
            exit_delta =  timedelta(hours=strg.hour, minutes=strg.minute)
            attendance.late_in = (enter_delta - exit_delta).total_seconds() / 3600.0
            #attendance.late_in = (AcDepart - t1).total_seconds() / 3600.0





    def action_deduction(self):
        for each in self:
            each.is_deduction = True

    def action_cancel_deduction(self):
        for each in self:
            each.is_deduction = False

    @api.depends('check_in','check_out')
    def _get_is_late_check(self):
      for each in self:
       if  each.check_in and each.check_out:
        localized_check_in = timezone('UTC').localize(each.check_in).astimezone(timezone(self.env.user.tz))
        localized_check_out = timezone('UTC').localize(each.check_out).astimezone(timezone(self.env.user.tz))
        weekday = localized_check_in.weekday()
        current_shift = each.employee_id.resource_calendar_id.attendance_ids.filtered(lambda a: a.dayofweek == str(weekday))
        each.late_price = 0
        if current_shift:
          if (localized_check_in.hour > current_shift.hour_from or
             (localized_check_in.hour == current_shift.hour_from and localized_check_in.minute >= 15)):
              each.is_late_check_in = True
              if each.check_in:
                  localized_check_in_officaly = localized_check_in.replace(minute=0, hour=int(current_shift.hour_from), second=0)
                  each.late_in_hours = (localized_check_in - localized_check_in_officaly).seconds / 3600
             #     each.late_price = (each.late_in_hours * each.employee_id.contract_id.gl)
          else:
              each.is_late_check_in = False

          if (localized_check_out.hour < (current_shift.hour_to - 1) or
             (localized_check_out.hour == (current_shift.hour_to - 1) and localized_check_out.minute <= 45)):
              each.is_early_check_out = True
              if each.check_out:
                 localized_check_out_officaly = localized_check_out.replace(minute=0, hour=int(current_shift.hour_to), second=0)
                 each.late_in_hours = (localized_check_out_officaly - localized_check_out).seconds / 3600
     #            each.late_price =each.late_price + (each.late_in_hours * each.employee_id.contract_id.gl)
          else:
              each.is_early_check_out = False

        else:
            each.is_late_check_in = False





    def _get_data_from_sql_server(self):
        driver = 'SQL Server'
     ##   driver = 'ODBC Driver 17 for SQL Server'
        server = '10.20.20.234'
        db = 'biotime'
        user = 'odoo'
        password = 'odoo@Paci221!'

        last_recored_upload_time = False
        attendances = self.env['hr.attendance'].search([], order='sql_Server_id_max desc')
        if attendances:
            last_recored_upload_time = attendances[0].sql_Server_id_max

        sql_query = """  
select top 1000  Id,CAST(CheckInemp_id as int) as Employee_Id ,CheckInTime,CheckOutTime,BreakInTime,BreakOutTime,BreakInTime2,BreakOutTime2,BreakInTime3,BreakOutTime3,OfficialInTime,OfficialOutTime,OfficialInTime2,OfficialOutTime2,OfficialInTime3,OfficialOutTime3,CheckInUploadTime,CheckOutUploadTime,BreakInUploadTime,BreakInUploadTime2,BreakInUploadTime3,BreakOutUploadTime,BreakOutUploadTime2,BreakOutUploadTime3,OfficialInUploadTime,OfficialInUploadTime2,OfficialInUploadTime3,OfficialOutUploadTime,OfficialOutUploadTime2,OfficialOutUploadTime3 from (

	select * from (
		----------------------------------------------------------------------------
	select * from (




        select * from (	   
              select * from (
                   select  min(Id) as Id, min(punch_time) as CheckInTime, CAST(punch_time as date) as CheckIn,emp_id as CheckInemp_id , min(Id) as CheckInUploadTime   from [biotime].[dbo].[iclock_transaction]  group by CAST(punch_time as date),punch_state,emp_id having punch_state =0
               ) checkin left outer join

        (select  max(punch_time) as CheckOutTime, CAST(punch_time as date) as CheckOut,emp_id as CheckOutemp_id, max(Id) as CheckOutUploadTime  from [biotime].[dbo].[iclock_transaction] group by CAST(punch_time as date),punch_state,emp_id having punch_state =1) Checkout 

        on checkin.CheckIn = Checkout.CheckOut and checkin.CheckInemp_id = Checkout.CheckOutemp_id
        ) CheckInOut

         left outer join 


         (
            select * from (
                   select min(punch_time) as BreakInTime,CAST(punch_time as date) as BreakIn,emp_id as BreakInemp_id, min(Id) as BreakInUploadTime  from [biotime].[dbo].[iclock_transaction]  group by CAST(punch_time as date),punch_state,emp_id having punch_state =3
               ) BreakIn left outer join

        (select min(punch_time) as BreakOutTime, CAST(punch_time as date) as BreakOut,emp_id as BreakOutemp_id, min(Id) as BreakOutUploadTime from [biotime].[dbo].[iclock_transaction]  group by CAST(punch_time as date),punch_state,emp_id having punch_state =4) BreakOut 

        on BreakIn.BreakIn = BreakOut.BreakOut and BreakIn.BreakInemp_id = BreakOut.BreakOutemp_id

         ) BreakInOut


         on  BreakInOut.BreakIn = CheckInOut.CheckIn and BreakInOut.BreakInemp_id = CheckInOut.CheckInemp_id


		 ) originalbiotime
	   ----------------------------------------------------------------------------


		   left outer join 

         (

		 ---------------------------------------------
            select * from (
                       select * from (
                         select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk, punch_time as BreakInTime2, CAST(punch_time as date) as BreakIn2,emp_id as BreakInemp_id2, Id as BreakInUploadTime2   , punch_state as BreakIn2punch_state
				            from [biotime].[dbo].[iclock_transaction] 
                        ) BreakTime2
				        WHERE  Rnk = 2  and BreakIn2punch_state =3
			  ) BreakIn2 left outer join

        (
		
		select * from (
		select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk2, punch_time as BreakOutTime2, CAST(punch_time as date) as BreakOut2,emp_id as BreakOutemp_id2, Id as BreakOutUploadTime2  , punch_state as BreakOut2punch_state
		
		from [biotime].[dbo].[iclock_transaction] 
		
		) BreakOut2
		 WHERE  Rnk2 = 2  and BreakOut2punch_state =4
		) 
		
		BreakOut2

        on BreakIn2.BreakIn2 = BreakOut2.BreakOut2 and BreakIn2.BreakInemp_id2 = BreakOut2.BreakOutemp_id2

		---------------------------------------

         ) BreakInOut2
         on  BreakInOut2.BreakIn2 = originalbiotime.CheckIn and BreakInOut2.BreakInemp_id2 = originalbiotime.CheckInemp_id
		 ) originalbiotime2


		 
		   left outer join 

         (

		 ---------------------------------------------

            select * from (
                       select * from (
                         select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk3, punch_time as BreakInTime3, CAST(punch_time as date) as BreakIn3,emp_id as BreakInemp_id3, Id as BreakInUploadTime3   , punch_state as BreakIn3punch_state
				            from [biotime].[dbo].[iclock_transaction] 
                        ) BreakTime3
				        WHERE  Rnk3 = 3  and BreakIn3punch_state =3
			  ) BreakIn3 left outer join

        (
		
		select * from (
		select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk32, punch_time as BreakOutTime3, CAST(punch_time as date) as BreakOut3,emp_id as BreakOutemp_id3, Id as BreakOutUploadTime3  , punch_state as BreakOut3punch_state
		
		from [biotime].[dbo].[iclock_transaction] 
		
		) BreakOut3
		 WHERE  Rnk32 = 3  and BreakOut3punch_state =4
		) 
		
		BreakOut3

        on BreakIn3.BreakIn3 = BreakOut3.BreakOut3 and BreakIn3.BreakInemp_id3 = BreakOut3.BreakOutemp_id3

	     ) BreakInOut3
         on  BreakInOut3.BreakIn3 = originalbiotime2.CheckIn and BreakInOut3.BreakInemp_id3 = originalbiotime2.CheckInemp_id
		 ) originalbiotime2
 




 
		 ---------------------------------------------

		   left outer join 

         (


		 
            select * from (
                       select * from (
                         select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk, punch_time as OfficialInTime, CAST(punch_time as date) as OfficialIn,emp_id as OfficialInemp_id, Id as OfficialInUploadTime   , punch_state as OfficialInpunch_state
				            from [biotime].[dbo].[iclock_transaction] 
                        ) OfficialTime
				        WHERE  Rnk = 1  and OfficialInpunch_state =4
			  ) OfficialIn left outer join

        (
		
		select * from (
		select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk2, punch_time as OfficialOutTime, CAST(punch_time as date) as OfficialOut,emp_id as OfficialOutemp_id, Id as OfficialOutUploadTime  , punch_state as OfficialOutpunch_state
		
		from [biotime].[dbo].[iclock_transaction] 
		
		) OfficialOut
		 WHERE  Rnk2 = 1  and OfficialOutpunch_state =5
		) 
		
		OfficialOut

        on OfficialIn.OfficialIn = OfficialOut.OfficialOut and OfficialIn.OfficialInemp_id = OfficialOut.OfficialOutemp_id

	     ) OfficialInOut
         on  OfficialInOut.OfficialIn = originalbiotime2.CheckIn and OfficialInOut.OfficialInemp_id = originalbiotime2.CheckInemp_id
	
  





  		   left outer join 

         (


		 
            select * from (
                       select * from (
                         select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk, punch_time as OfficialInTime2, CAST(punch_time as date) as OfficialIn,emp_id as OfficialInemp_id, Id as OfficialInUploadTime2   , punch_state as OfficialInpunch_state
				            from [biotime].[dbo].[iclock_transaction] 
                        ) OfficialTime
				        WHERE  Rnk = 2  and OfficialInpunch_state =4
			  ) OfficialIn left outer join

        (
		
		select * from (
		select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk2, punch_time as OfficialOutTime2, CAST(punch_time as date) as OfficialOut,emp_id as OfficialOutemp_id, Id as OfficialOutUploadTime2  , punch_state as OfficialOutpunch_state
		
		from [biotime].[dbo].[iclock_transaction] 
		
		) OfficialOut
		 WHERE  Rnk2 = 2  and OfficialOutpunch_state =5
		) 
		
		OfficialOut

        on OfficialIn.OfficialIn = OfficialOut.OfficialOut and OfficialIn.OfficialInemp_id = OfficialOut.OfficialOutemp_id

	     ) OfficialInOut2
         on  OfficialInOut2.OfficialIn = originalbiotime2.CheckIn and OfficialInOut2.OfficialInemp_id = originalbiotime2.CheckInemp_id
	
  
  
 

  		   left outer join 

         (


		 
            select * from (
                       select * from (
                         select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk, punch_time as OfficialInTime3, CAST(punch_time as date) as OfficialIn,emp_id as OfficialInemp_id, Id as OfficialInUploadTime3   , punch_state as OfficialInpunch_state
				            from [biotime].[dbo].[iclock_transaction] 
                        ) OfficialTime
				        WHERE  Rnk = 3  and OfficialInpunch_state =4
			  ) OfficialIn left outer join

        (
		
		select * from (
		select row_number() OVER (Partition By CAST(punch_time as date),punch_state,emp_id ORDER BY punch_time ) Rnk2, punch_time as OfficialOutTime3, CAST(punch_time as date) as OfficialOut,emp_id as OfficialOutemp_id, Id as OfficialOutUploadTime3  , punch_state as OfficialOutpunch_state
		
		from [biotime].[dbo].[iclock_transaction] 
		
		) OfficialOut
		 WHERE  Rnk2 = 3  and OfficialOutpunch_state =5
		) 
		
		OfficialOut

        on OfficialIn.OfficialIn = OfficialOut.OfficialOut and OfficialIn.OfficialInemp_id = OfficialOut.OfficialOutemp_id

	     ) OfficialInOut3
         on  OfficialInOut3.OfficialIn = originalbiotime2.CheckIn and OfficialInOut3.OfficialInemp_id = originalbiotime2.CheckInemp_id
        """

        if last_recored_upload_time:
            sql_query += "where CheckInUploadTime > " + str(last_recored_upload_time) + " or CheckOutUploadTime > " + str(last_recored_upload_time) +" or BreakInUploadTime > " + str(last_recored_upload_time) +" or BreakOutUploadTime > " + str(last_recored_upload_time) +" or BreakInUploadTime2 > " + str(last_recored_upload_time)+" or BreakInUploadTime3 > " + str(last_recored_upload_time)+" or BreakOutUploadTime2 > " + str(last_recored_upload_time)+" or BreakOutUploadTime3 > " + str(last_recored_upload_time) + " or OfficialInUploadTime > " + str(last_recored_upload_time) +" or OfficialOutUploadTime > " + str(last_recored_upload_time) +" or OfficialInUploadTime2 > " + str(last_recored_upload_time)+" or OfficialInUploadTime3 > " + str(last_recored_upload_time)+" or OfficialOutUploadTime2 > " + str(last_recored_upload_time)+" or OfficialOutUploadTime3 > " + str(last_recored_upload_time)


        sql_query+=" order by CheckInUploadTime,CheckOutUploadTime,BreakInUploadTime,BreakOutUploadTime,BreakInUploadTime2,BreakOutUploadTime2,BreakInUploadTime3,BreakOutUploadTime3,OfficialInUploadTime,OfficialOutUploadTime,OfficialInUploadTime2,OfficialOutUploadTime2,OfficialInUploadTime3,OfficialOutUploadTime3"
        conn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % (driver, server, db, user, password))
        cursor = conn.cursor()
        return cursor.execute(sql_query)

    def _update_company_last_attendants_schedule_work(self, total):
        today = datetime.today()
        companies = self.env['res.company'].search([])
        for company in companies:
            if company.id == self.env.company.id:
                company.last_attendants_schedule_work_date = today
                company.last_attendants_schedule_work_total = total



    @api.model
    def _fetch_attendance_from_sql_server(self):

        rowsNumber=0
        cursor = self._get_data_from_sql_server()
        #while(cursor):
        for row in cursor:
                if row.Employee_Id == 53:
                  continue
                employee_id = self.env['hr.employee'].search([('id', '=', row.Employee_Id)])

                if employee_id:
                    checkInTime = row.CheckInTime
                    checkOutTime = row.CheckOutTime
                    breakInTime = row.BreakInTime
                    breakOutTime = row.BreakOutTime
                    breakInTime2 = row.BreakInTime2
                    breakOutTime2 = row.BreakOutTime2
                    breakInTime3 = row.BreakInTime3
                    breakOutTime3 = row.BreakOutTime3
                    officialInTime = row.OfficialInTime
                    officialOutTime = row.OfficialOutTime
                    officialInTime2 = row.OfficialInTime2
                    officialOutTime2 = row.OfficialOutTime2
                    officialInTime3 = row.OfficialInTime3
                    officialOutTime3 = row.OfficialOutTime3

                    max_upload_time = row.CheckInUploadTime
                    check_in_id = row.CheckInUploadTime
                    if row.CheckInTime and row.CheckOutTime and row.CheckInTime > row.CheckOutTime:
                        checkInTime = row.CheckOutTime
                        checkOutTime = row.CheckInTime
                    if row.BreakInTime and row.BreakOutTime and row.BreakInTime > row.BreakOutTime:
                        breakInTime = row.BreakOutTime
                        breakOutTime = row.BreakInTime
                    if row.BreakInTime2 and row.BreakOutTime2 and row.BreakInTime2 > row.BreakOutTime2:
                        breakInTime2 = row.BreakOutTime2
                        breakOutTime2 = row.BreakInTime2
                    if row.BreakInTime3 and row.BreakOutTime3 and row.BreakInTime3 > row.BreakOutTime3:
                        breakInTime3 = row.BreakOutTime3
                        breakOutTime3 = row.BreakInTime3

                    if row.OfficialInTime and row.OfficialOutTime and row.OfficialInTime > row.OfficialOutTime:
                        officialInTime = row.OfficialOutTime
                        officialOutTime = row.OfficialInTime
                    if row.OfficialInTime2 and row.OfficialOutTime2 and row.OfficialInTime2 > row.OfficialOutTime2:
                        officialInTime2 = row.OfficialOutTime2
                        officialOutTime2 = row.OfficialInTime2
                    if row.OfficialInTime3 and row.OfficialOutTime3 and row.OfficialInTime3 > row.OfficialOutTime3:
                        officialInTime3 = row.OfficialOutTime3
                        officialOutTime3 = row.OfficialInTime3

                    if row.CheckInTime and not row.CheckOutTime:
                        checkOutTime = row.CheckInTime

                    if row.CheckOutUploadTime:
                        if not max_upload_time or (max_upload_time and row.CheckOutUploadTime > max_upload_time):
                            max_upload_time = row.CheckOutUploadTime

                    if row.BreakInUploadTime:
                        if not max_upload_time or (max_upload_time and row.BreakInUploadTime > max_upload_time):
                            max_upload_time = row.BreakInUploadTime

                    if row.BreakOutUploadTime:
                        if not max_upload_time or (max_upload_time and row.BreakOutUploadTime > max_upload_time):
                            max_upload_time = row.BreakOutUploadTime

                    if row.BreakInUploadTime2:
                        if not max_upload_time or (max_upload_time and row.BreakInUploadTime2 > max_upload_time):
                            max_upload_time = row.BreakInUploadTime2

                    if row.BreakOutUploadTime2:
                        if not max_upload_time or (max_upload_time and row.BreakOutUploadTime2 > max_upload_time):
                            max_upload_time = row.BreakOutUploadTime2

                    if row.BreakInUploadTime3:
                        if not max_upload_time or (max_upload_time and row.BreakInUploadTime3 > max_upload_time):
                            max_upload_time = row.BreakInUploadTime3

                    if row.BreakOutUploadTime3:
                        if not max_upload_time or (max_upload_time and row.BreakOutUploadTime3 > max_upload_time):
                            max_upload_time = row.BreakOutUploadTime3




                    if row.OfficialInUploadTime:
                        if not max_upload_time or (max_upload_time and row.OfficialInUploadTime > max_upload_time):
                            max_upload_time = row.OfficialInUploadTime

                    if row.OfficialOutUploadTime:
                        if not max_upload_time or (max_upload_time and row.OfficialOutUploadTime > max_upload_time):
                            max_upload_time = row.OfficialOutUploadTime

                    if row.OfficialInUploadTime2:
                        if not max_upload_time or (max_upload_time and row.OfficialInUploadTime2 > max_upload_time):
                            max_upload_time = row.OfficialInUploadTime2

                    if row.OfficialOutUploadTime2:
                        if not max_upload_time or (max_upload_time and row.OfficialOutUploadTime2 > max_upload_time):
                            max_upload_time = row.OfficialOutUploadTime2

                    if row.OfficialInUploadTime3:
                        if not max_upload_time or (max_upload_time and row.OfficialInUploadTime3 > max_upload_time):
                            max_upload_time = row.OfficialInUploadTime3

                    if row.OfficialOutUploadTime3:
                        if not max_upload_time or (max_upload_time and row.OfficialOutUploadTime3 > max_upload_time):
                            max_upload_time = row.OfficialOutUploadTime3





                    attendance = self.env['hr.attendance'].search([('sql_Server_check_in_id', '=', check_in_id)])
                    if attendance:
                       attendance.unlink()

                    self.env["hr.attendance"].create(
                        {
                            "employee_id": row.Employee_Id,
                            "check_in": checkInTime,
                            "check_out": checkOutTime,
                            "break_in": breakInTime,
                            "break_out": breakOutTime,
                            "official_in": officialInTime,
                            "official_out": officialOutTime,
                            "sql_Server_id_max": max_upload_time,
                            "sql_Server_check_in_id": check_in_id,
                            "break_in_2": breakInTime2,
                            "break_in_3": breakInTime3,
                            "break_out_2": breakOutTime2,
                            "break_out_3": breakOutTime3,
                            "official_in_2": officialInTime2,
                            "official_out_2": officialOutTime2,
                            "official_in_3": officialInTime3,
                            "official_out_3": officialOutTime3,
                            "area_name": "HQ"
                        }
                    )
                    rowsNumber+=1
            #self.env.cr.commit()
            #cursor = self._get_data_from_sql_server()
        self._update_company_last_attendants_schedule_work(rowsNumber)



class Holiday(models.Model):

    _inherit = "hr.leave"
    sql_Server_id = fields.Integer(readonly=True)


    @api.model
    def _fetch_holiday_from_sql_server(self):

        rowsNumber=0
        cursor = self._get_holiday_from_sql_server()
        for row in cursor:
                if row.employee_id > 53:
                  continue
                employee_id = self.env['hr.employee'].search([('id', '=', row.employee_id)])
                leave_type_id = self.env['hr.leave.type'].search([('code', '=', row.category_code)])

                if employee_id:
                    start_time = row.start_time
                    end_time = row.end_time
                    apply_reason = row.apply_reason
                    apply_time = row.apply_time
                    approval_level = row.approval_level
                    approver = row.approver
                    employee_id = row.employee_id
                    category_id = row.category_id
                    category_code = row.category_code
                    self.env["hr.leave"].create(
                        {
                            "employee_id": employee_id,
                            "date_from": start_time,
                            "date_to": end_time,
                            "reason": apply_reason,
                            "holiday_status_id": leave_type_id.id,
                            "create_date": apply_time,
                            "sql_Server_id": row.abstractexception_ptr_id
                        }
                    )
                    rowsNumber+=1

    def _get_holiday_from_sql_server(self):
        driver = 'SQL Server'
        ##   driver = 'ODBC Driver 17 for SQL Server'
        server = '10.20.20.234'
        db = 'biotime'
        user = 'odoo'
        password = 'odoo@Paci221!'

        last_recored_upload_time = False
        leaves = self.env['hr.leave'].search([], order='sql_Server_id desc')
        if leaves:
            last_recored_upload_time = leaves[0].sql_Server_id

        sql_query = """   SELECT TOP (1000) [abstractexception_ptr_id]
      ,[start_time]
      ,[end_time]
      ,[apply_reason]
      ,[apply_time]
      ,[approval_level]
      ,[approver]
	  , CASE WHEN category_id = 1 THEN 'BL'
	         WHEN category_id = 2 THEN 'PL'
			 WHEN category_id = 3 THEN 'AV'
			 WHEN category_id = 4 THEN 'SV'
			 WHEN category_id = 5 THEN 'ML'
			 WHEN category_id = 6 THEN 'BT'
         END AS [category_code]
      ,[category_id]
      ,[employee_id]
  FROM [biotime].[dbo].[att_leave]
            """

        if last_recored_upload_time:
            sql_query += "where abstractexception_ptr_id > " + str(last_recored_upload_time)

        sql_query += " order by apply_time"
        conn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % (driver, server, db, user, password))
        cursor = conn.cursor()
        return cursor.execute(sql_query)
