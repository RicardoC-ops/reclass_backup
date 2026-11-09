import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const SUPABASE_URL = 'https://mggntdrbjbojflihpeae.supabase.co';

const SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_7JLgIGTQwNKnJQRJclT0wg_G6PTc3zy';

export const supabase = createClient(
    SUPABASE_URL,
    SUPABASE_PUBLISHABLE_KEY
);