# Copyright (c) 2025, DataWits Information Technology Ltd. and Contributors
# License: MIT. See LICENSE

import json
from typing import Dict, List, Any, Optional

import frappe
import frappe.utils

@frappe.whitelist(allow_guest=True)
def get_iot_cnc_data(equipment_id=None, limit=50, offset=0):
	"""
	External API to retrieve CNC data from IoT Management module
	
	Args:
		equipment_id (str, optional): Filter by specific equipment ID
		limit (int): Number of records to return (default: 50, max: 1000)
		offset (int): Number of records to skip (default: 0)
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: List of CNC data records
		- total_count: Total number of records matching the filter
		- message: Status message
	"""
	try:
		# Validate parameters
		limit = min(max(int(limit), 1), 1000)  # Ensure limit is between 1 and 1000
		offset = max(int(offset), 0)  # Ensure offset is non-negative
		
		# Build filters
		filters = {}
		if equipment_id:
			filters["equipmentid"] = equipment_id
		
		# Get total count for pagination
		total_count = frappe.db.count("CNCData", filters)
		
		# Fetch CNC data records
		fields = [
			"name",
			"equipmentid",
			"workpiececount", 
			"runtime",
			"cuttingtime",
			"cncmodel",
			"currenttoolno",
			"operationmode",
			"runmode",
			"rapidoverride",
			"spindleactualrpm",
			"feedactualrate",
			"spindleload",
			"xaxisload",
			"yaxisload",
			"zaxisload",
			"alarmcode",
			"alarmmessage",
			"creation",
			"modified"
		]
		
		cnc_data = frappe.db.get_all(
			"CNCData",
			filters=filters,
			fields=fields,
			order_by="modified desc",
			limit=limit,
			start=offset
		)
		
		# Format response data
		formatted_data = []
		for record in cnc_data:
			formatted_record = {
				"id": record.get("name"),
				"equipment_id": record.get("equipmentid"),
				"workpiece_count": record.get("workpiececount"),
				"runtime": record.get("runtime"),
				"cutting_time": record.get("cuttingtime"),
				"cnc_model": record.get("cncmodel"),
				"current_tool_no": record.get("currenttoolno"),
				"operation_mode": record.get("operationmode"),
				"run_mode": record.get("runmode"),
				"rapid_override": record.get("rapidoverride"),
				"spindle_actual_rpm": record.get("spindleactualrpm"),
				"feed_actual_rate": record.get("feedactualrate"),
				"spindle_load": record.get("spindleload"),
				"x_axis_load": record.get("xaxisload"),
				"y_axis_load": record.get("yaxisload"),
				"z_axis_load": record.get("zaxisload"),
				"alarm_code": record.get("alarmcode"),
				"alarm_message": record.get("alarmmessage"),
				"created_at": record.get("creation"),
				"updated_at": record.get("modified")
			}
			formatted_data.append(formatted_record)
		
		return {
			"success": True,
			"data": formatted_data,
			"total_count": total_count,
			"returned_count": len(formatted_data),
			"offset": offset,
			"limit": limit,
			"message": f"Successfully retrieved {len(formatted_data)} CNC data records"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": "CNCData DocType not found. Please ensure IoT Management module is installed."
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_cnc_data: {str(e)}", "API Error")
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": f"An error occurred while retrieving CNC data: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_cnc_data_by_id(cnc_data_id):
	"""
	External API to retrieve a specific CNC data record by ID
	
	Args:
		cnc_data_id (str): The ID of the CNC data record
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: CNC data record details
		- message: Status message
	"""
	try:
		if not cnc_data_id:
			return {
				"success": False,
				"data": None,
				"message": "CNC data ID is required"
			}
		
		# Fetch specific CNC data record
		cnc_data = frappe.get_doc("CNCData", cnc_data_id)
		
		formatted_data = {
			"id": cnc_data.name,
			"equipment_id": cnc_data.get("equipmentid"),
			"workpiece_count": cnc_data.get("workpiececount"),
			"runtime": cnc_data.get("runtime"),
			"cutting_time": cnc_data.get("cuttingtime"),
			"cnc_model": cnc_data.get("cncmodel"),
			"current_tool_no": cnc_data.get("currenttoolno"),
			"operation_mode": cnc_data.get("operationmode"),
			"run_mode": cnc_data.get("runmode"),
			"rapid_override": cnc_data.get("rapidoverride"),
			"spindle_actual_rpm": cnc_data.get("spindleactualrpm"),
			"feed_actual_rate": cnc_data.get("feedactualrate"),
			"spindle_load": cnc_data.get("spindleload"),
			"x_axis_load": cnc_data.get("xaxisload"),
			"y_axis_load": cnc_data.get("yaxisload"),
			"z_axis_load": cnc_data.get("zaxisload"),
			"alarm_code": cnc_data.get("alarmcode"),
			"alarm_message": cnc_data.get("alarmmessage"),
			"created_at": cnc_data.creation,
			"updated_at": cnc_data.modified,
			"created_by": cnc_data.owner,
			"modified_by": cnc_data.modified_by
		}
		
		return {
			"success": True,
			"data": formatted_data,
			"message": "Successfully retrieved CNC data record"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": None,
			"message": f"CNC data record with ID '{cnc_data_id}' not found"
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_cnc_data_by_id: {str(e)}", "API Error")
		return {
			"success": False,
			"data": None,
			"message": f"An error occurred while retrieving CNC data: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_equipment_list():
	"""
	External API to get list of unique equipment IDs from CNC data
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: List of unique equipment IDs
		- message: Status message
	"""
	try:
		# Get unique equipment IDs
		equipment_ids = frappe.db.get_all(
			"CNCData",
			fields=["equipmentid"],
			group_by="equipmentid",
			order_by="equipmentid"
		)
		
		# Extract just the IDs and filter out empty values
		equipment_list = [
			item["equipmentid"] for item in equipment_ids 
			if item.get("equipmentid")
		]
		
		return {
			"success": True,
			"data": equipment_list,
			"count": len(equipment_list),
			"message": f"Successfully retrieved {len(equipment_list)} unique equipment IDs"
		}
		
	except Exception as e:
		frappe.log_error(f"Error in get_iot_equipment_list: {str(e)}", "API Error")
		return {
			"success": False,
			"data": [],
			"count": 0,
			"message": f"An error occurred while retrieving equipment list: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_maintenance_history(equipment_id=None, limit=50, offset=0):
	"""
	External API to retrieve maintenance history data from IoT Management module
	
	Args:
		equipment_id (str, optional): Filter by specific equipment ID  
		limit (int): Number of records to return (default: 50, max: 1000)
		offset (int): Number of records to skip (default: 0)
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: List of maintenance history records
		- total_count: Total number of records matching the filter
		- message: Status message
	"""
	try:
		# Validate parameters
		limit = min(max(int(limit), 1), 1000)  # Ensure limit is between 1 and 1000
		offset = max(int(offset), 0)  # Ensure offset is non-negative
		
		# Build filters
		filters = {}
		if equipment_id:
			filters["equipmentid"] = equipment_id
		
		# Get total count for pagination
		total_count = frappe.db.count("RMMSMaintenanceHistory", filters)
		
		# Fetch maintenance history records
		fields = [
			"name",
			"maintenanceid",
			"equipmentid",
			"maintenancedate",
			"maintenancetype",
			"description",
			"replacedparts",
			"downtimeminutes",
			"creation",
			"modified"
		]
		
		maintenance_data = frappe.db.get_all(
			"RMMSMaintenanceHistory",
			filters=filters,
			fields=fields,
			order_by="modified desc",
			limit=limit,
			start=offset
		)
		
		# Format response data
		formatted_data = []
		for record in maintenance_data:
			formatted_record = {
				"id": record.get("name"),
				"maintenance_id": record.get("maintenanceid"),
				"equipment_id": record.get("equipmentid"),
				"maintenance_date": record.get("maintenancedate"),
				"maintenance_type": record.get("maintenancetype"),
				"description": record.get("description"),
				"replaced_parts": record.get("replacedparts"),
				"downtime_minutes": record.get("downtimeminutes"),
				"created_at": record.get("creation"),
				"updated_at": record.get("modified")
			}
			formatted_data.append(formatted_record)
		
		return {
			"success": True,
			"data": formatted_data,
			"total_count": total_count,
			"returned_count": len(formatted_data),
			"offset": offset,
			"limit": limit,
			"message": f"Successfully retrieved {len(formatted_data)} maintenance history records"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": "RMMSMaintenanceHistory DocType not found. Please ensure IoT Management module is installed."
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_maintenance_history: {str(e)}", "API Error")
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": f"An error occurred while retrieving maintenance history: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_maintenance_history_by_id(maintenance_history_id):
	"""
	External API to retrieve a specific maintenance history record by ID
	
	Args:
		maintenance_history_id (str): The ID of the maintenance history record
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: Maintenance history record details
		- message: Status message
	"""
	try:
		if not maintenance_history_id:
			return {
				"success": False,
				"data": None,
				"message": "Maintenance history ID is required"
			}
		
		# Fetch specific maintenance history record
		maintenance_data = frappe.get_doc("RMMSMaintenanceHistory", maintenance_history_id)
		
		formatted_data = {
			"id": maintenance_data.name,
			"maintenance_id": maintenance_data.get("maintenanceid"),
			"equipment_id": maintenance_data.get("equipmentid"),
			"maintenance_date": maintenance_data.get("maintenancedate"),
			"maintenance_type": maintenance_data.get("maintenancetype"),
			"description": maintenance_data.get("description"),
			"replaced_parts": maintenance_data.get("replacedparts"),
			"downtime_minutes": maintenance_data.get("downtimeminutes"),
			"created_at": maintenance_data.creation,
			"updated_at": maintenance_data.modified,
			"created_by": maintenance_data.owner,
			"modified_by": maintenance_data.modified_by
		}
		
		return {
			"success": True,
			"data": formatted_data,
			"message": "Successfully retrieved maintenance history record"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": None,
			"message": f"Maintenance history record with ID '{maintenance_history_id}' not found"
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_maintenance_history_by_id: {str(e)}", "API Error")
		return {
			"success": False,
			"data": None,
			"message": f"An error occurred while retrieving maintenance history: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_failure_cases(equipment_model=None, limit=50, offset=0):
	"""
	External API to retrieve failure cases data from IoT Management module
	
	Args:
		equipment_model (str, optional): Filter by specific equipment model
		limit (int): Number of records to return (default: 50, max: 1000)
		offset (int): Number of records to skip (default: 0)
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: List of failure cases records
		- total_count: Total number of records matching the filter
		- message: Status message
	"""
	try:
		# Validate parameters
		limit = min(max(int(limit), 1), 1000)  # Ensure limit is between 1 and 1000
		offset = max(int(offset), 0)  # Ensure offset is non-negative
		
		# Build filters
		filters = {}
		if equipment_model:
			filters["equipmentmodel"] = equipment_model
		
		# Get total count for pagination
		total_count = frappe.db.count("RMMSFailureCases", filters)
		
		# Fetch failure cases records
		fields = [
			"name",
			"caseid",
			"equipmentmodel",
			"symptom",
			"failuremode",
			"rootcause",
			"correctiveaction",
			"requiredparts",
			"creation",
			"modified"
		]
		
		failure_data = frappe.db.get_all(
			"RMMSFailureCases",
			filters=filters,
			fields=fields,
			order_by="modified desc",
			limit=limit,
			start=offset
		)
		
		# Format response data
		formatted_data = []
		for record in failure_data:
			formatted_record = {
				"id": record.get("name"),
				"case_id": record.get("caseid"),
				"equipment_model": record.get("equipmentmodel"),
				"symptom": record.get("symptom"),
				"failure_mode": record.get("failuremode"),
				"root_cause": record.get("rootcause"),
				"corrective_action": record.get("correctiveaction"),
				"required_parts": record.get("requiredparts"),
				"created_at": record.get("creation"),
				"updated_at": record.get("modified")
			}
			formatted_data.append(formatted_record)
		
		return {
			"success": True,
			"data": formatted_data,
			"total_count": total_count,
			"returned_count": len(formatted_data),
			"offset": offset,
			"limit": limit,
			"message": f"Successfully retrieved {len(formatted_data)} failure cases records"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": "RMMSFailureCases DocType not found. Please ensure IoT Management module is installed."
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_failure_cases: {str(e)}", "API Error")
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": f"An error occurred while retrieving failure cases: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_failure_cases_by_id(failure_case_id):
	"""
	External API to retrieve a specific failure case record by ID
	
	Args:
		failure_case_id (str): The ID of the failure case record
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: Failure case record details
		- message: Status message
	"""
	try:
		if not failure_case_id:
			return {
				"success": False,
				"data": None,
				"message": "Failure case ID is required"
			}
		
		# Fetch specific failure case record
		failure_data = frappe.get_doc("RMMSFailureCases", failure_case_id)
		
		formatted_data = {
			"id": failure_data.name,
			"case_id": failure_data.get("caseid"),
			"equipment_model": failure_data.get("equipmentmodel"),
			"symptom": failure_data.get("symptom"),
			"failure_mode": failure_data.get("failuremode"),
			"root_cause": failure_data.get("rootcause"),
			"corrective_action": failure_data.get("correctiveaction"),
			"required_parts": failure_data.get("requiredparts"),
			"created_at": failure_data.creation,
			"updated_at": failure_data.modified,
			"created_by": failure_data.owner,
			"modified_by": failure_data.modified_by
		}
		
		return {
			"success": True,
			"data": formatted_data,
			"message": "Successfully retrieved failure case record"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": None,
			"message": f"Failure case record with ID '{failure_case_id}' not found"
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_failure_cases_by_id: {str(e)}", "API Error")
		return {
			"success": False,
			"data": None,
			"message": f"An error occurred while retrieving failure case: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_equipment_models_list():
	"""
	External API to get list of unique equipment models from failure cases
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: List of unique equipment models
		- message: Status message
	"""
	try:
		# Get unique equipment models
		equipment_models = frappe.db.get_all(
			"RMMSFailureCases",
			fields=["equipmentmodel"],
			group_by="equipmentmodel",
			order_by="equipmentmodel"
		)
		
		# Extract just the models and filter out empty values
		models_list = [
			item["equipmentmodel"] for item in equipment_models 
			if item.get("equipmentmodel")
		]
		
		return {
			"success": True,
			"data": models_list,
			"count": len(models_list),
			"message": f"Successfully retrieved {len(models_list)} unique equipment models"
		}
		
	except Exception as e:
		frappe.log_error(f"Error in get_iot_equipment_models_list: {str(e)}", "API Error")
		return {
			"success": False,
			"data": [],
			"count": 0,
			"message": f"An error occurred while retrieving equipment models list: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_production_data(equipment_id=None, limit=50, offset=0):
	"""
	External API to retrieve production data from IoT Management module
	
	Args:
		equipment_id (str, optional): Filter by specific equipment ID
		limit (int): Number of records to return (default: 50, max: 1000)
		offset (int): Number of records to skip (default: 0)
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: List of production data records
		- total_count: Total number of records matching the filter
		- message: Status message
	"""
	try:
		# Validate parameters
		limit = min(max(int(limit), 1), 1000)  # Ensure limit is between 1 and 1000
		offset = max(int(offset), 0)  # Ensure offset is non-negative
		
		# Build filters
		filters = {}
		if equipment_id:
			filters["equipmentid"] = equipment_id
		
		# Get total count for pagination
		total_count = frappe.db.count("MESProductionData", filters)
		
		# Fetch production data records
		fields = [
			"name",
			"workorderid",
			"equipmentid",
			"productid",
			"productname",
			"plannedquantity",
			"actualquantity",
			"starttime",
			"endtime",
			"operatorid",
			"creation",
			"modified"
		]
		
		production_data = frappe.db.get_all(
			"MESProductionData",
			filters=filters,
			fields=fields,
			order_by="modified desc",
			limit=limit,
			start=offset
		)
		
		# Format response data
		formatted_data = []
		for record in production_data:
			formatted_record = {
				"id": record.get("name"),
				"work_order_id": record.get("workorderid"),
				"equipment_id": record.get("equipmentid"),
				"product_id": record.get("productid"),
				"product_name": record.get("productname"),
				"planned_quantity": record.get("plannedquantity"),
				"actual_quantity": record.get("actualquantity"),
				"start_time": record.get("starttime"),
				"end_time": record.get("endtime"),
				"operator_id": record.get("operatorid"),
				"created_at": record.get("creation"),
				"updated_at": record.get("modified")
			}
			formatted_data.append(formatted_record)
		
		return {
			"success": True,
			"data": formatted_data,
			"total_count": total_count,
			"returned_count": len(formatted_data),
			"offset": offset,
			"limit": limit,
			"message": f"Successfully retrieved {len(formatted_data)} production data records"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": "MESProductionData DocType not found. Please ensure IoT Management module is installed."
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_production_data: {str(e)}", "API Error")
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": f"An error occurred while retrieving production data: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_production_data_by_id(production_data_id):
	"""
	External API to retrieve a specific production data record by ID
	
	Args:
		production_data_id (str): The ID of the production data record
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: Production data record details
		- message: Status message
	"""
	try:
		if not production_data_id:
			return {
				"success": False,
				"data": None,
				"message": "Production data ID is required"
			}
		
		# Fetch specific production data record
		production_data = frappe.get_doc("MESProductionData", production_data_id)
		
		formatted_data = {
			"id": production_data.name,
			"work_order_id": production_data.get("workorderid"),
			"equipment_id": production_data.get("equipmentid"),
			"product_id": production_data.get("productid"),
			"product_name": production_data.get("productname"),
			"planned_quantity": production_data.get("plannedquantity"),
			"actual_quantity": production_data.get("actualquantity"),
			"start_time": production_data.get("starttime"),
			"end_time": production_data.get("endtime"),
			"operator_id": production_data.get("operatorid"),
			"created_at": production_data.creation,
			"updated_at": production_data.modified,
			"created_by": production_data.owner,
			"modified_by": production_data.modified_by
		}
		
		return {
			"success": True,
			"data": formatted_data,
			"message": "Successfully retrieved production data record"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": None,
			"message": f"Production data record with ID '{production_data_id}' not found"
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_production_data_by_id: {str(e)}", "API Error")
		return {
			"success": False,
			"data": None,
			"message": f"An error occurred while retrieving production data: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_work_orders_list():
	"""
	External API to get list of unique work order IDs from production data
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: List of unique work order IDs
		- message: Status message
	"""
	try:
		# Get unique work order IDs
		work_orders = frappe.db.get_all(
			"MESProductionData",
			fields=["workorderid"],
			group_by="workorderid",
			order_by="workorderid"
		)
		
		# Extract just the IDs and filter out empty values
		work_orders_list = [
			item["workorderid"] for item in work_orders 
			if item.get("workorderid")
		]
		
		return {
			"success": True,
			"data": work_orders_list,
			"count": len(work_orders_list),
			"message": f"Successfully retrieved {len(work_orders_list)} unique work order IDs"
		}
		
	except Exception as e:
		frappe.log_error(f"Error in get_iot_work_orders_list: {str(e)}", "API Error")
		return {
			"success": False,
			"data": [],
			"count": 0,
			"message": f"An error occurred while retrieving work orders list: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_spare_parts(part_id=None, limit=50, offset=0):
	"""
	External API to retrieve spare parts data from IoT Management module
	
	Args:
		part_id (str, optional): Filter by specific part ID
		limit (int): Number of records to return (default: 50, max: 1000)
		offset (int): Number of records to skip (default: 0)
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: List of spare parts records
		- total_count: Total number of records matching the filter
		- message: Status message
	"""
	try:
		# Validate parameters
		limit = min(max(int(limit), 1), 1000)  # Ensure limit is between 1 and 1000
		offset = max(int(offset), 0)  # Ensure offset is non-negative
		
		# Build filters
		filters = {}
		if part_id:
			filters["partid"] = part_id
		
		# Get total count for pagination
		total_count = frappe.db.count("RMMSSpareParts", filters)
		
		# Fetch spare parts records
		fields = [
			"name",
			"partid",
			"partname",
			"description",
			"applicablemodel",
			"supplier",
			"stockquantity",
			"unitprice",
			"leadtimedays",
			"creation",
			"modified"
		]
		
		spare_parts_data = frappe.db.get_all(
			"RMMSSpareParts",
			filters=filters,
			fields=fields,
			order_by="modified desc",
			limit=limit,
			start=offset
		)
		
		# Format response data
		formatted_data = []
		for record in spare_parts_data:
			formatted_record = {
				"id": record.get("name"),
				"part_id": record.get("partid"),
				"part_name": record.get("partname"),
				"description": record.get("description"),
				"applicable_model": record.get("applicablemodel"),
				"supplier": record.get("supplier"),
				"stock_quantity": record.get("stockquantity"),
				"unit_price": record.get("unitprice"),
				"lead_time_days": record.get("leadtimedays"),
				"created_at": record.get("creation"),
				"updated_at": record.get("modified")
			}
			formatted_data.append(formatted_record)
		
		return {
			"success": True,
			"data": formatted_data,
			"total_count": total_count,
			"returned_count": len(formatted_data),
			"offset": offset,
			"limit": limit,
			"message": f"Successfully retrieved {len(formatted_data)} spare parts records"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": "RMMSSpareParts DocType not found. Please ensure IoT Management module is installed."
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_spare_parts: {str(e)}", "API Error")
		return {
			"success": False,
			"data": [],
			"total_count": 0,
			"returned_count": 0,
			"offset": offset,
			"limit": limit,
			"message": f"An error occurred while retrieving spare parts: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_spare_parts_by_id(spare_part_id):
	"""
	External API to retrieve a specific spare part record by ID
	
	Args:
		spare_part_id (str): The ID of the spare part record
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: Spare part record details
		- message: Status message
	"""
	try:
		if not spare_part_id:
			return {
				"success": False,
				"data": None,
				"message": "Spare part ID is required"
			}
		
		# Fetch specific spare part record
		spare_part_data = frappe.get_doc("RMMSSpareParts", spare_part_id)
		
		formatted_data = {
			"id": spare_part_data.name,
			"part_id": spare_part_data.get("partid"),
			"part_name": spare_part_data.get("partname"),
			"description": spare_part_data.get("description"),
			"applicable_model": spare_part_data.get("applicablemodel"),
			"supplier": spare_part_data.get("supplier"),
			"stock_quantity": spare_part_data.get("stockquantity"),
			"unit_price": spare_part_data.get("unitprice"),
			"lead_time_days": spare_part_data.get("leadtimedays"),
			"created_at": spare_part_data.creation,
			"updated_at": spare_part_data.modified,
			"created_by": spare_part_data.owner,
			"modified_by": spare_part_data.modified_by
		}
		
		return {
			"success": True,
			"data": formatted_data,
			"message": "Successfully retrieved spare part record"
		}
		
	except frappe.DoesNotExistError:
		return {
			"success": False,
			"data": None,
			"message": f"Spare part record with ID '{spare_part_id}' not found"
		}
	except Exception as e:
		frappe.log_error(f"Error in get_iot_spare_parts_by_id: {str(e)}", "API Error")
		return {
			"success": False,
			"data": None,
			"message": f"An error occurred while retrieving spare part: {str(e)}"
		}

@frappe.whitelist(allow_guest=True)
def get_iot_suppliers_list():
	"""
	External API to get list of unique suppliers from spare parts
	
	Returns:
		Dict containing:
		- success: Boolean indicating operation success
		- data: List of unique suppliers
		- message: Status message
	"""
	try:
		# Get unique suppliers
		suppliers = frappe.db.get_all(
			"RMMSSpareParts",
			fields=["supplier"],
			group_by="supplier",
			order_by="supplier"
		)
		
		# Extract just the suppliers and filter out empty values
		suppliers_list = [
			item["supplier"] for item in suppliers 
			if item.get("supplier")
		]
		
		return {
			"success": True,
			"data": suppliers_list,
			"count": len(suppliers_list),
			"message": f"Successfully retrieved {len(suppliers_list)} unique suppliers"
		}
		
	except Exception as e:
		frappe.log_error(f"Error in get_iot_suppliers_list: {str(e)}", "API Error")
		return {
			"success": False,
			"data": [],
			"count": 0,
			"message": f"An error occurred while retrieving suppliers list: {str(e)}"
		}