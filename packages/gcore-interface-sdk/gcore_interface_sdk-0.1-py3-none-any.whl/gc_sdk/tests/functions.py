def start_weigh_round_test(main_controller):
        info = {'info':{'record_id': 2,
         'carnum': 'А333АА333',
         'carrier': 1,
         'trash_cat': 5,
         'trash_type': 4,
         'comm': 'INITTED FROM API',
         'course': 'IN',
         'car_choose_mode': 'manual',
         'dlinnomer': 0,
         'polomka': 0,
         'orup_mode': 'extended',
         'operator': 1,
         'carnum_was': 'А333АА333',
         'polygon_object': 'ТКО-ТЕСТ'}}
        main_controller.start_weight_round(**info)


def change_opened_record_test(main_controller):
    main_controller.change_opened_record(record_id=3, car_number='А333АА333', comment='CHANGED FROM SDK', trash_cat=1,
                                         trash_type=5, carrier=1)


def add_comment_test(main_controller):
    main_controller.add_comment(record_id=2, comment='ADDED FROM SDK')


def close_opened_record_test(main_controller):
    main_controller.execute_method(method_name='close_opened_record', record_id=3)
