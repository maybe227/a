import sys,os, glob
from backend.common_policy import *
from backend.common_show import *
from common.parse_case import *
from cfp.cfp_run import *

if __name__ == "__main__":
	case_file_path = "../case/show/"
	f = open(ShowCaseXML.caseId_orderitemId_rel_file, "w")
	f.flush()
	f.close()
	
	#do cfp
	if os.path.isdir(case_file_path):
		case_file_list = os.listdir(case_file_path)
		for item in case_file_list:
			if item[-4:] != ".xml":
				continue
			case_file = "%s%s" %(case_file_path,item)
			print case_file
			cfp = CFP_Runner()
			cfp.runtest(case_file,ShowCaseXML.caseId_orderitemId_rel_file)
	time.sleep(120)
	
	#do show
	if os.path.isdir(case_file_path):
		case_file_list = os.listdir(case_file_path)
		for item in case_file_list:
			if item[-4:] != ".xml":
				continue
			case_file = "%s%s" %(case_file_path,item)
			case = ShowCaseXML(case_file)
			case_count = case.get_cases_count()
			print "case num = %d" %case_count
			i = 1
			while i <= case_count:
				case.init_case(i)
				player = case.get_request_player()
				video = case.get_request_video()
				policy = BasePolicyInterface(player,video,0,0,"")
				policy.request()
				if policy.is_policy_no_ads() == 1:
					print "no policy"
					sys.exit()
				cuepointList = policy.get_cuepoint_list()
				show = BaseShowInterface(player,video,"","","")
				show.request(cuepointList)
				if show.is_show_no_ads() == 1:
					print "show response none"
					sys.exit()
				actual_orderitem_num = show.get_orderitem_num()
    
				expect_orderitem_list = case.get_expect_orderitem()
				num = 0
				orderitems = []
				while num < actual_orderitem_num:
					orderitems.append(show.get_orderitem_id(num))
					num = num + 1
				#print show.get_show_response()
				#time.sleep(5)
				print orderitems
				print expect_orderitem_list
				if orderitems in expect_orderitem_list:
					print "PASS"
				else:
					print "FAIL"
				i = i + 1