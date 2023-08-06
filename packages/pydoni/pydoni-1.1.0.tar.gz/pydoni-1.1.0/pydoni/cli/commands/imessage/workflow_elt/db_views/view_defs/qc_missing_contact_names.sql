drop view if exists imessage.qc_missing_contact_names;

create or replace view imessage.qc_missing_contact_names as

select
   m.message_uid
   , m.chat_identifier
   , m.message_date
   , m."text"
   , m.source
   , m.is_from_me
from
   imessage.message_vw m
left join
   imessage.contact_names_ignored i
   on m.chat_identifier = i.chat_identifier
where
   m.message_date > current_date - 35  -- Andoni manually checks this view every ~30 days, so no need to review the same texts multiple times
   and i.chat_identifier is null
   and m.contact_name is null
   and m.is_text = true
   and not m.chat_identifier ~ '^\d{5,6}$'  -- Phone number of 5-6 digits is typically automated