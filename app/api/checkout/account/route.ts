import { accountAccessConfig } from "@/lib/checkout/account-config";
import { saveCheckoutAccount } from "@/lib/checkout/account-handler";
export const dynamic = "force-dynamic";
export async function POST(request: Request) { return saveCheckoutAccount(request, accountAccessConfig()); }
