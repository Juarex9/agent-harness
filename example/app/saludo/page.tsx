import { greet } from "@/lib/greet";

type SaludoSearchParams = {
  name?: string | string[];
};

export default async function SaludoPage({
  searchParams,
}: {
  searchParams: Promise<SaludoSearchParams>;
}) {
  const params = await searchParams;
  const raw = params.name;
  const name = Array.isArray(raw) ? raw[0] : raw;

  return (
    <main>
      <h1>{greet(name)}</h1>
    </main>
  );
}
