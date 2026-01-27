Django project with Vue Front End

As an application owner
I want to advance front end tools
so that an improved user experience is realized and a more maintainable source code base is in place

---

## Feature: Project Structures & Parts Management

### User Story
As a user, I want to view all structures for a given project and see all parts within each structure, so that I can schedule and ship parts efficiently.

### Requirements

#### View
- Display a list of all structures belonging to a selected project
- Within each structure, show all associated parts
- Parts should display relevant details (name, status, etc.)

#### Actions
- **Schedule** a part - mark a part as scheduled for work/delivery
- **Ship** a part - mark a part as shipped

### Data Model

```
Project
  ├── id
  ├── name
  └── description

Structure
  ├── id
  ├── project (FK → Project)
  ├── name
  └── description

PartDetail
  ├── id
  ├── structure (FK → Structure)
  ├── name
  ├── price (decimal)
  ├── takeoff_url (S3 link)
  ├── quantity (integer)
  ├── weight (decimal)
  └── is_released (boolean)

Part (physical instance, 1:1 with RFID) [FUTURE SCOPE]
  ├── id
  ├── part_detail (FK → PartDetail)
  ├── rfid (string, unique)
  └── created_at (datetime)
  Note: Used later for logging pours and truck loading, not linked at schedule/ship time

ScheduleEvent
  ├── id
  ├── part_detail (FK → PartDetail)
  ├── scheduled_date (date)
  ├── scheduled_time (time)
  ├── quantity (integer)
  ├── part_identifier (string) ← can differ from original
  ├── price (decimal) ← can differ from original
  └── created_at (datetime)

ShippingEvent
  ├── id
  ├── shipped_date (datetime)
  ├── notes (text, nullable)
  └── created_at (datetime)

ShippingPart
  ├── id
  ├── shipping_event (FK → ShippingEvent)
  ├── part_detail (FK → PartDetail)
  ├── quantity (integer) ← can be subset of part_detail.quantity
  └── weight (decimal) ← captured at time of shipment
```

### Business Rules
1. **Only released part details** can be scheduled or shipped
2. **Scheduling**: One part detail at a time; creates a ScheduleEvent record
   - Quantity can be specified (how many to pour/make)
   - Part identifier and price can be modified when adding to schedule
   - Requires both date and time
   - A part detail can be scheduled multiple times (e.g., repours after issues)
3. **Shipping**: Multiple part details shipped together in one ShippingEvent
   - Creates ShippingPart records linked to the event
   - Quantity shipped can be a subset of part_detail.quantity
   - A part detail can be shipped multiple times (e.g., replacements, partial shipments)
   - Display total weight of selected part details before confirming
4. **Scheduling is NOT required for shipping**
   - Stock parts can be shipped directly without being scheduled

### API Endpoints (Proposed)
- `GET /api/projects/` - list all projects
- `GET /api/projects/<id>/structures/` - list structures for a project with nested part details
- `POST /api/schedule-events/` - schedule a part detail (body: part_detail_id, date, time, quantity, part_identifier, price)
- `POST /api/shipping-events/` - create shipment with multiple part details (body: list of {part_detail_id, quantity, weight})
- `GET /api/shipping-events/` - list shipping events with totals

### UI Components (Proposed)
- **ProjectSelector** - dropdown to choose active project
- **StructureList** - expandable list of structures
- **PartDetailList** - part details within a structure showing:
  - Name, price, quantity, weight
  - Link to takeoff (S3)
  - Release status indicator
  - Checkbox for bulk ship selection
- **ScheduleModal** - form for scheduling a single part detail
  - Date picker, time picker
  - Quantity field
  - Editable part identifier and price fields
- **ShipAction** - ship button showing total weight of selected part details

### PartDetail Display Fields
| Field | Description |
|-------|-------------|
| Name | Part detail name |
| Price | Unit price (editable during scheduling) |
| Quantity | Number of units |
| Weight | Weight per unit |
| Takeoff | Link to S3 document |
| Status | Released / Not Released |

---

## Implementation Status

### Completed
- [x] Django app `projects` with models: Project, Structure, PartDetail, ScheduleEvent, ShippingEvent, ShippingPart
- [x] Admin interface with inline editing
- [x] API endpoints:
  - `GET /api/projects/`
  - `GET /api/projects/<id>/structures/`
  - `POST /api/schedule-events/`
  - `POST /api/shipping-events/create/`
  - `GET /api/shipping-events/`
- [x] Vue components:
  - ProjectSelector
  - StructureList (with expandable structures and part details table)
  - ScheduleModal
  - ShipAction

### To Test
1. Run Django server: `cd src && python manage.py runserver`
2. Create test data via admin: `/admin/`
3. View the app at: `/`

### Future Scope
- [ ] Part table with RFID tracking (for pour logging and truck loading) 

